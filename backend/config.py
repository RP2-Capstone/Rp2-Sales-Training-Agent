import os
from dotenv import load_dotenv

load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL   = "gemini-1.5-flash"   


FORCE_USE_LLM = None   # True = always use LLM
                       # False = never use LLM (fallback only)
                       # None = auto detect from API key

if FORCE_USE_LLM is True:
    USE_LLM = True
elif FORCE_USE_LLM is False:
    USE_LLM = False
else:
    USE_LLM = bool(GEMINI_API_KEY)   # ✅ auto mode using Gemini key


VOICE_ENABLED  = True
VOICE_LANGUAGE = "en"       # language for gTTS
VOICE_SPEED    = False      # False = normal speed, True = slow


DB_PATH = "sales_training.db"


APP_HOST = "0.0.0.0"
APP_PORT = 8000
DEBUG    = True