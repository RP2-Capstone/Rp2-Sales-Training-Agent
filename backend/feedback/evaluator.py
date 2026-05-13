import json
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL, USE_LLM


if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        generation_config={
            "temperature":     0.2,    # low = more consistent scoring
            "max_output_tokens": 500,
        }
    )
else:
    model = None


def fallback_evaluation(conversation_history):
    """Simple rule-based evaluation when Gemini is not available"""
    turns = len(conversation_history)

    return {
        "score": min(10, turns),
        "strengths": [
            "Maintained conversation flow",
            "Engaged with the student"
        ],
        "weaknesses": [
            "Limited analysis (no AI evaluation)"
        ],
        "suggestions": [
            "Enable AI evaluation for detailed feedback",
            "Ask more probing questions"
        ]
    }

# ✅ Load sentiment model
try:
    from transformers import pipeline
    sentiment_analyzer = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )
    ML_AVAILABLE = True
    print("✅ ML Sentiment model loaded")
except ImportError:
    ML_AVAILABLE = False
    print("⚠️ ML not available - skipping sentiment")
except Exception as e:           # ✅ catches other errors
    ML_AVAILABLE = False
    print(f"⚠️ ML loading failed: {e}")


def build_chat_text(conversation_history):
    """Convert conversation history list into readable text"""
    chat_text = ""
    for turn in conversation_history:
        chat_text += f"Salesperson: {turn['salesperson']}\n"
        chat_text += f"Student:     {turn['student']}\n\n"
    return chat_text


def build_prompt(chat_text):
    return f"""
You are a strict and professional sales trainer
evaluating a sales trainee's performance.

Conversation:
{chat_text}

Evaluate EACH skill separately and give individual scores:

1. Communication Clarity  (0-10) - Clear and easy to understand?
2. Confidence             (0-10) - Spoke with confidence?
3. Objection Handling     (0-10) - Handled student doubts well?
4. Product Knowledge      (0-10) - Knew the course details?
5. Closing Ability        (0-10) - Tried to close or move forward?

Rules:
- Be strict and realistic
- Score 0-4 = Poor, 5-6 = Average, 7-8 = Good, 9-10 = Excellent
- Base score on actual conversation only
- If skill was not demonstrated → score 3 or below

Return ONLY valid JSON, no markdown, no extra text:
{{
  "overall_score": <average of all 5 scores>,
  "skill_scores": {{
    "communication":    <0-10>,
    "confidence":       <0-10>,
    "objection_handling": <0-10>,
    "product_knowledge": <0-10>,
    "closing_ability":  <0-10>
  }},
  "strengths":   ["specific strength from conversation"],
  "weaknesses":  ["specific weakness from conversation"],
  "suggestions": ["specific actionable suggestion"]
}}
"""

def detect_sales_keywords(conversation_history):
    """
    Detect good and bad sales keywords
    used by the salesperson
    """

    # ✅ Words good salespeople use
    GOOD_KEYWORDS = {
        "benefit":      "Focused on benefits",
        "value":        "Highlighted value",
        "imagine":      "Used visualization",
        "because":      "Gave reasons",
        "guarantee":    "Gave assurance",
        "opportunity":  "Created opportunity",
        "for example":  "Used examples",
        "you will":     "Student focused",
        "limited":      "Created urgency",
        "understand":   "Showed empathy"
    }

    # ❌ Words weak salespeople use
    BAD_KEYWORDS = {
        "i don't know": "Showed uncertainty",
        "maybe":        "Lacked confidence",
        "not sure":     "Lacked knowledge",
        "i think":      "Unsure of facts",
        "whatever":     "Showed disinterest",
        "complicated":  "Made it sound hard",
        "expensive":    "Focused on price negatively",
        "difficult":    "Negative framing"
    }

    # Combine all salesperson messages
    full_text = " ".join([
        turn["salesperson"].lower()
        for turn in conversation_history
    ])

    # Find matches
    good_found = {
        k: v for k, v in GOOD_KEYWORDS.items()
        if k in full_text
    }
    bad_found = {
        k: v for k, v in BAD_KEYWORDS.items()
        if k in full_text
    }

    # Calculate keyword score
    keyword_score = min(10, max(0,
        len(good_found) * 1.5 - len(bad_found) * 2
    ))

    return {
        "keyword_score":  round(keyword_score, 1),
        "good_keywords":  good_found,
        "bad_keywords":   bad_found
    }

def analyze_sentiment(conversation_history):
    """
    Analyze tone of salesperson messages
    Returns tone score and breakdown
    """
    if not ML_AVAILABLE:
        return None

    results = []

    for turn in conversation_history:
        message = turn["salesperson"][:512]   # limit length

        try:
            result = sentiment_analyzer(message)[0]
            results.append({
                "message":    message[:50] + "...",
                "tone":       result["label"],
                "confidence": round(result["score"], 2)
            })
        except:
            continue

    if not results:
        return None

    # Count positive vs negative
    positive = sum(1 for r in results if r["tone"] == "POSITIVE")
    negative = len(results) - positive

    tone_score = round((positive / len(results)) * 10, 1)

    return {
        "tone_score":        tone_score,
        "positive_messages": positive,
        "negative_messages": negative,
        "total_messages":    len(results),
        "breakdown":         results
    }


def clean_json_response(text):
    """
    Gemini sometimes wraps response in markdown
    This strips it before parsing

    Example input:
```json
    { "score": 8 ... }
```
    Example output:
    { "score": 8 ... }
    """
    text = text.strip()

    # ✅ Remove markdown code fences if present
    if text.startswith("```"):
        text = text.split("```")[1]         # remove opening ```
        if text.startswith("json"):
            text = text[4:]                 # remove the word "json"

    return text.strip()


def evaluate_conversation(
    conversation_history,
    mode: str = "recent"
):
    # ✅ Select history based on mode
    if mode == "full":
        history = conversation_history
    else:
        history = conversation_history[-10:]

    # ✅ No API → fallback
    if model is None or not USE_LLM:
        print("⚠️ Gemini not available")
        return fallback_evaluation(history)

    try:
        
        chat_text    = build_chat_text(history)
        prompt       = build_prompt(chat_text)
        response     = model.generate_content(prompt)
        cleaned      = clean_json_response(response.text)
        gemini_result = json.loads(cleaned)

        gemini_score = gemini_result.get("overall_score", 5)

        keyword_result = detect_sales_keywords(history)
        keyword_score  = keyword_result["keyword_score"]

        tone_result = analyze_sentiment(history)
        tone_score  = tone_result["tone_score"] if tone_result else gemini_score

        final_score = round(
            gemini_score  * 0.60 +
            keyword_score * 0.20 +
            tone_score    * 0.20,
            1
        )

        return {
            # ✅ Scores
            "final_score":   final_score,
            "gemini_score":  gemini_score,
            "keyword_score": keyword_score,
            "tone_score":    tone_score,

            # ✅ Per skill breakdown
            "skill_scores":  gemini_result.get("skill_scores", {}),

            # ✅ Feedback
            "strengths":     gemini_result.get("strengths",   []),
            "weaknesses":    gemini_result.get("weaknesses",  []),
            "suggestions":   gemini_result.get("suggestions", []),

            # ✅ Detailed analysis
            "keyword_analysis": keyword_result,
            "tone_analysis":    tone_result
        }

    except json.JSONDecodeError as e:
        print("JSON Error:", e)
        return fallback_evaluation(history)

    except Exception as e:
        print("Evaluation Error:", e)
        return fallback_evaluation(history)