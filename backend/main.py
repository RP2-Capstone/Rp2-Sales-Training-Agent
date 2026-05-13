from fastapi import FastAPI
from fastapi.responses import FileResponse
from rag_engine import search
from voice.text_to_speech import convert_text_to_speech
from llm_engine import generate_response
from feedback.evaluator import evaluate_conversation
from pathlib import Path
from pydantic import BaseModel

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🧠 Store full conversation
conversation_history = []

# 🏠 Home route
@app.get("/")
def home():
    return {"message": "Backend is working successfully"}

class ChatRequest(BaseModel):
    message: str
    persona: str = "Beginner"
    course: str = ""

# 💬 Chat endpoint (Salesperson ↔ AI Student)
@app.post("/chat")
def chat(user_message: ChatRequest):
    try:
        message = user_message.message
        selected_persona = user_message.persona
        selected_course = user_message.course

        if not message:
            return {"error": "Message cannot be empty"}

        if not selected_course:
            return {"error": "Course must be selected"}

        print("User:", message)

        # ✅ FIXED INDENTATION
        if len(conversation_history) == 0:
            message = f"{selected_course} course introduction. User said: {message}"

        # 🔍 RAG search
        results = search(
            query=f"{selected_course} {message}",
            persona=selected_persona
        )

        if results and len(results) > 0:
            top_result = results[0]
            print("RAG Top Result:", top_result)

            retrieved_text = top_result.get("answer", "")
            persona = selected_persona

            response_text = generate_response(
                user_message=message,
                retrieved_text=f"Course: {selected_course}\n{retrieved_text}",
                persona=persona,
                history=conversation_history
            )

        else:
            print("No result")
            response_text = f"Hmm… I didn’t quite get that. Can you explain a bit more about the {selected_course} course?"

        # 🧠 Store conversation
        conversation_history.append({
            "salesperson": message,
            "student": response_text
        })

        # Limit history
        conversation_history[:] = conversation_history[-10:]

        # 🔊 Generate voice
        audio_file = convert_text_to_speech(response_text)
        audio_url = f"/audio/{audio_file}" if audio_file else None

        return {
            "response": response_text,
            "audio_url": audio_file
        }

    except Exception as e:
        print("Error:", e)
        return {"error": "Something went wrong in the backend"}

# 🔊 Audio endpoint
@app.get("/audio/{filename}")
def get_audio(filename: str):
    file_path = Path("audio") / filename

    if not file_path.exists():
        return {"error": "Audio file not found"}

    return FileResponse(file_path, media_type="audio/mpeg")
   
# 📊 Evaluate full conversation
@app.get("/evaluate")
def evaluate():
    if not conversation_history:
        return {"error": "No conversation to evaluate"}

    result = evaluate_conversation(conversation_history[-10:])

    import json

    try:
        parsed = json.loads(result)
    except:
        parsed = {"raw": result}

    return parsed

# 🔁 Reset conversation
@app.post("/reset")
def reset():
    conversation_history.clear()
    return {"message": "Conversation reset successfully"}
