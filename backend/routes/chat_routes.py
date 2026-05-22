from fastapi import APIRouter
from pydantic import BaseModel
from b_config import USE_LLM
import random
import string

def generate_session_id():
    chars = string.ascii_uppercase + string.digits
    code  = "".join(random.choices(chars, k=5))
    return f"RP2-{code}"

router = APIRouter()

class ChatRequest(BaseModel):
    message:    str
    persona:    str = ""
    course:     str = ""
    session_id: str = ""


def fallback_response(user_input, course, rag_text=None):
    if rag_text:
        return f"{rag_text} (Let me know if you want more details!)"
    return (
        f"Thanks for your question about the {course} course! "
        "This program covers everything step-by-step with practical examples. "
        "Would you like to know about syllabus, tools, or career opportunities?"
    )


@router.post("/")                          
def chat(user_message: ChatRequest):
    try:
        
        from database import get_conversation, save_conversation
        from ai_logic.rag import search
        from ai_logic.llm import get_llm_response
        from ai_logic.chatbot import get_response
        from voice.text_to_speech import convert_text_to_speech

        # ✅ Extract fields
        message          = user_message.message
        selected_persona = user_message.persona
        selected_course  = user_message.course

        # ✅ Generate session_id if not provided
        session_id = user_message.session_id or generate_session_id()

        # ✅ Validate inputs
        if not message:
            return {"error": "Message cannot be empty"}
        if not selected_course:
            return {"error": "Course must be selected"}

        # ✅ Get THIS student's history
        conversation_history = get_conversation(session_id)

        
        # 🔍 RAG search
        retrieved_text = search(message)

        if retrieved_text and len(retrieved_text) > 0:
            top_result     = retrieved_text[0]
            retrieved_text = top_result.get("answer", "")

            if USE_LLM:
                response_text = get_llm_response(
                    user_message   = message,
                    retrieved_text = f"Course: {selected_course}\n{retrieved_text}",
                    persona        = selected_persona,
                    history        = conversation_history
                )
            else:
                response_text = fallback_response(message,selected_course,retrieved_text)
        else:
            response_text = get_response(
                 user_message=message,
                 persona=selected_persona,
                 history=conversation_history,
                 session_id=session_id,
                 course=selected_course
            )

        # ✅ Save THIS student's conversation
        save_conversation(
            session_id      = session_id,
            salesperson_msg = message,
            student_msg     = response_text,
            persona         = selected_persona,
            course          = selected_course
        )

        # 🔊 Generate voice
        audio_file = convert_text_to_speech(response_text)
        audio_url  = f"/voice/audio/{audio_file}" if audio_file else None

        # ✅ Return response + session_id back to frontend
        return {
            "response":   response_text,
            "audio_url":  audio_url,
            "session_id": session_id
        }

    except Exception as e:
        print("Error:", e)
        return {"error": "Something went wrong in the backend"}
    
@router.get("/history/{session_id}")
def get_chat_history(session_id: str):
    """Return full conversation history for a session"""
    try:
        from database import get_conversation
        history = get_conversation(session_id=session_id, limit=999)
        return {"session_id": session_id, "history": history}
    except Exception as e:
        print("History Error:", e)
        return {"error": "Could not fetch history"}
