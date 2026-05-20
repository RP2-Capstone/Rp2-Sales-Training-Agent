from openai import OpenAI
from ai_logic.config import OPENAI_API_KEY, USE_LLM

client = None

if USE_LLM:
    client = OpenAI(api_key=OPENAI_API_KEY)


def ask_llm(prompt):

    if not USE_LLM:
        return None

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        print("LLM Error:", e)
        return None