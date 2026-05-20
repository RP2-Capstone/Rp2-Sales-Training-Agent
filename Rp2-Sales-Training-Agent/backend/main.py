
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routes.chat_routes import router as chat_router
from routes.feedback_routes import router as feedback_router
from routes.voice_routes import router as voice_router
from database import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ సర్వర్ స్టార్ట్ అయినప్పుడు రన్ అవుతుంది (డేటాబేస్ టేబుల్స్ క్రియేట్ చేస్తుంది)
    print("🚀 Starting AI Sales Coach Backend...")
    try:
        create_tables()
        print("📊 Database tables checked/created successfully.")
    except Exception as e:
        print("❌ Database initialization error:", e)
    yield
    # ✅ సర్వర్ స్టాప్ అయినప్పుడు రన్ అవుతుంది
    print("🛑 Shutting down AI Sales Coach Backend...")


app = FastAPI(
    title="AI Sales Coach Backend",
    version="1.0.0",
    lifespan=lifespan
)

# 🌐 CORS Middleware: ఫ్రంటెండ్ (Streamlit) నుండి వచ్చే రిక్వెస్ట్‌లను అనుమతించడానికి
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # డెవలప్‌మెంట్ స్టేజ్‌లో అన్ని ఆరిజిన్స్‌ని అనుమతిస్తున్నాం
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, OPTIONS అన్ని మెథడ్స్ అనుమతి
    allow_headers=["*"],
)

# 🛠️ ROUTERS INCLUSION
# ఇక్కడ prefix="/chat" ఇవ్వడం వల్ల ఫుల్ URL: http://127.0.0.1:8000/chat/ అవుతుంది
app.include_router(chat_router,     prefix="/chat",     tags=["Chat"])
app.include_router(feedback_router, prefix="/feedback", tags=["Feedback"])
app.include_router(voice_router,    prefix="/voice",    tags=["Voice"])


@app.get("/")
def home():
    """
    సర్వర్ ఆన్‌లో ఉందో లేదో బ్రౌజర్‌లో డైరెక్ట్‌గా చెక్ చేసుకోవడానికి హోమ్ రూట్
    """
    return {
        "status": "online",
        "message": "AI Sales Coach Backend is running successfully"
    }


@app.post("/reset")
def reset(session_id: str):
    """
    స్టూడెంట్ చాట్ హిస్టరీని రీసెట్ చేయడానికి ఎండ్‌పాయింట్
    """
    try:
        from database import clear_conversation
        clear_conversation(session_id)
        return {"message": "Conversation reset successfully", "session_id": session_id}
    except Exception as e:
        return {"error": f"Failed to reset conversation: {str(e)}"}