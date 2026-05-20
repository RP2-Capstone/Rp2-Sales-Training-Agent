import os
from groq import Groq

from dotenv import load_dotenv

# .env ఫైల్ నుండి కీ ని లోడ్ చేస్తుంది
load_dotenv()

# కోడ్ లో కీ ని నేరుగా రాయకుండా ఇలా పిలుచుకో
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

def get_ai_response(message: str, combined_info: dict, history: str):
    persona = combined_info.get("name", "Beginner")
    course = combined_info.get("course", "Data Science")
    
    system_prompt = f"""
  
    You are a prospective student interested in {course}. 
YOU ARE NOT A SALESPERSON. YOU ARE THE CUSTOMER.
- Your Goal: You want to learn {course}, but you are hesitant about the price and want to be convinced.
- Your Tone: Skeptical, curious, and price-sensitive. 
- Rules: 
    1. NEVER sell the course back to the user. 
    2. ALWAYS ask questions like: "Is it worth the money?", "Can I get a better discount?", "How can I trust your placement support?".
    3. Be the "Interested Student" who needs that final push to pay.
"""
    
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Previous conversation:\n{history}\n\nNew Message: {message}"}
        ],
        temperature=0.7
    )
    return completion.choices[0].message.content

def get_final_feedback(conversation_history: str):
    """సెషన్ ముగిశాక ఫైనల్ రిపోర్ట్ కోసం """
    system_prompt = """
    You are an expert Sales Manager. Analyze the following conversation between a Salesperson and a Prospective Student.
    Provide:
    1. Overall Score (1-10) [cite: 21]
    2. Strengths of the salesperson.
    3. Areas of improvement regarding communication, clarity, and handling objections[cite: 21].
    4. Final verdict on conversion readiness.
    """
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": conversation_history}],
        temperature=0.7
    )
    return completion.choices[0].message.content
