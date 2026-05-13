
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_llm_response(user_message, persona, history):
    return "LLM is disabled right now. Using local AI system."

