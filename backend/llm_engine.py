import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not set")

client = OpenAI(api_key=api_key)

def generate_response(user_message, retrieved_text, persona, history):

    history_text = ""
    for turn in history:
        history_text += f"Salesperson: {turn['salesperson']}\n"
        history_text += f"Student: {turn['student']}\n"

    persona_behavior = {
        "Beginner": "knows nothing and asks simple questions",
        "Intermediate": "has some knowledge and asks logical questions",
        "Expert": "asks deep, critical and challenging questions"
    }

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"""
You are a {persona} student on a phone call.

Behavior:
{persona_behavior.get(persona)}

Rules:
- Speak casually like a human
- Keep responses short (1–2 lines)
- Ask follow-up questions
- Avoid repeating questions
- Show curiosity, doubt, or interest
- Never sound like an AI
"""
                },
                {
                    "role": "user",
                    "content": f"""
Course Info:
{retrieved_text}

Conversation so far:
{history_text}

Salesperson: {user_message}

Respond as the student and continue the conversation naturally.
"""
                }
            ],
            temperature=0.7,
            max_tokens=100
        )

        return response.choices[0].message.content

    except Exception as e:
        print("LLM Error:", e)
        return f"[{persona} Student] Sorry, I didn't understand. Could you explain again?"
