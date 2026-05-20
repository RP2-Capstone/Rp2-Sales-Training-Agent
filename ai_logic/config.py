import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

USE_LLM = OPENAI_API_KEY is not None and OPENAI_API_KEY != ""