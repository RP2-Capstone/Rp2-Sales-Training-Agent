import os
from groq import Groq

from dotenv import load_dotenv

# .env ఫైల్ నుండి కీ ని లోడ్ చేస్తుంది
load_dotenv()

# కోడ్ లో కీ ని నేరుగా రాయకుండా ఇలా పిలుచుకో
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

def get_ai_response(message: str, combined_info: dict, history: str):
    """AI స్టూడెంట్ రెస్పాన్స్ కోసం"""
    persona = combined_info.get("name", "Beginner")
    course = combined_info.get("course", "Data Science")
    
    system_prompt = f"""
    You are a prospective student interested in {course} at RP2. Persona: {persona}.
    Your goal is to ask questions about course structure, duration, fees, and placement support[cite: 10, 12, 15, 16, 17].
    Act like a real student, simulate objections, and follow-up questions[cite: 18, 19].
    Keep responses concise and natural. Do NOT provide feedback yet.
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
