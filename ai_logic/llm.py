import os
from groq import Groq
from dotenv import load_dotenv

# .env ఫైల్ లోడ్ చేయడానికి
load_dotenv()

# ✅ ఇక్కడ కీ టెక్స్ట్ డైరెక్ట్ గా ఇచ్చేస్తున్నాం, దీనివల్ల ఎలాంటి లోడింగ్ ప్రాబ్లం ఉండదు!

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def get_llm_response(user_message, persona, history):
    """
    Groq API ని ఉపయోగించి రెస్పాన్స్ జనరేట్ చేసే పక్కా ఫంక్షన్.
    """
    try:
        # హిస్టరీ మరియు పర్సోనాని బేస్ చేసుకుని ప్రాंప్ట్ బిల్డ్ చేస్తున్నాం
        messages = [
            {"role": "system", "content": f"You are a sales training assistant acting as the following persona: {persona}"}
        ]
        
        # పాత చాట్ హిస్టరీని యాడ్ చేస్తున్నాం
        for msg in history:
            if isinstance(msg, dict) and "role" in msg and "content" in msg:
                messages.append(msg)
            
        # లేటెస్ట్ యూజర్ మెసేజ్ యాడ్ చేస్తున్నాం
        messages.append({"role": "user", "content": user_message})
        
        # Groq Llama 3 మోడల్ ని కాల్ చేస్తున్నాం
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )
        
        return completion.choices[0].message.content
        
    except Exception as e:
        print("❌ Error inside llm.py:", e)
        return f"Error connecting to Groq AI: {str(e)}"

