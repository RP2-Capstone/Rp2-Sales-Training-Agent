import json
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def evaluate_conversation(conversation_history):
    recent_history = conversation_history[-10:]

    chat_text = ""
    for turn in recent_history:
        chat_text += f"Salesperson: {turn['salesperson']}\n"
        chat_text += f"Student: {turn['student']}\n\n"

    prompt = f"""
Evaluate the salesperson based on:
1. Communication clarity
2. Confidence
3. Handling objections
4. Product knowledge
5. Closing ability

Conversation:
{chat_text}

Return JSON only:
{{
  "score": number (0-10),
  "strengths": ["point1", "point2"],
  "weaknesses": ["point1", "point2"],
  "suggestions": ["point1", "point2"]
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a strict and professional sales trainer. Always return valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=200,
            response_format={"type": "json_object"}
        )

        output = response.choices[0].message.content

        return json.loads(output)

    except Exception as e:
        print("Evaluation Error:", e)
        return {
            "score": 0,
            "strengths": [],
            "weaknesses": ["Evaluation failed"],
            "suggestions": ["Try again later"]
        }
