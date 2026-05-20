
from fastapi import APIRouter
from pydantic import BaseModel
import uuid

router = APIRouter()

class ChatRequest(BaseModel):
    message:    str
    persona:    str = "Beginner"
    course:     str = ""
    session_id: str = ""

@router.post("/")
def chat(user_message: ChatRequest):
    try:
        from ai_logic.llm import get_llm_response

        message          = user_message.message
        selected_persona = user_message.persona
        selected_course  = user_message.course
        session_id       = user_message.session_id or str(uuid.uuid4())

        # Groq API ని పిలుస్తున్నాం
        response_text = get_llm_response(
            user_message   = message,
            persona        = selected_persona,
            history        = []
        )

        # ఒకవేళ Groq నుండి రెస్పాన్స్ రాకపోతే బ్యాకప్ టెక్స్ట్ ఇక్కడ ఇస్తున్నాం
        if not response_text or "Error" in response_text:
            response_text = f"Hello! I am a {selected_persona} student. Thanks for offering the {selected_course} course! Can you explain it simply?"

        return {
            "response":   response_text,
            "audio_url":  None,
            "session_id": session_id,
            "score":      7  # app.py లో స్కోర్ ఎర్రర్ రాకుండా డమ్మీ స్కోర్
        }

    except Exception as e:
        return {
            "response":   f"Hello! I want to learn {selected_course}. Let's start!",
            "audio_url":  None,
            "session_id": session_id,
            "score":      6
        }