
import streamlit as st
from streamlit_mic_recorder import speech_to_text
from services.api_client import get_ai_response, get_final_feedback
from frontend_logic.persona_config import PERSONAS, COURSES
from gtts import gTTS
import base64
import os
import tempfile


# Page Config
st.set_page_config(page_title="RP2 AI Sales Trainer", layout="wide", page_icon="🛡️")

# --- Updated Audio Function ---

def autoplay_audio(text):
    if not text: return
    try:
        tts = gTTS(text=text, lang='en')
        # Temporary file ని క్రియేట్ చేసి పాత్ ని సేవ్ చేస్తున్నాం
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            file_path = fp.name # ఇక్కడ డిఫైన్ చేశాను
            
        # ఇప్పుడు st.audio లో ఆ పాత్ ని వాడుతున్నాం
        st.audio(file_path, format="audio/mp3", autoplay=True)
            
    except Exception as e:
        st.error(f"Audio Error: {e}")




# Session State
if "messages" not in st.session_state: st.session_state.messages = []
if "history" not in st.session_state: st.session_state.history = ""
if "mic_counter" not in st.session_state: st.session_state.mic_counter = 0

# Sidebar
with st.sidebar:
    st.header("Configuration")
    selected_p_name = st.selectbox("Select Persona:", list(PERSONAS.keys()))
    selected_course = st.selectbox("Choose Course:", COURSES)
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.history = ""
        st.rerun()

st.title("🛡️ RP2 Sales Training - Professional Edition")

# --- Chat Messages ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- INPUT HANDLING ---
col1, col2 = st.columns([0.9, 0.1])
with col1:
    prompt = st.chat_input("Type your pitch here...")
with col2:
    # Salesperson (Mic Input)
    audio_text = speech_to_text(key=f"mic_{st.session_state.mic_counter}", use_container_width=True)

user_input = None
if prompt:
    user_input = prompt
elif audio_text:
    user_input = audio_text
    st.session_state.mic_counter += 1

# Process Input
# Process Input బ్లాక్ లో:
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    combined_info = {**PERSONAS[selected_p_name], "name": selected_p_name, "course": selected_course}
    
    with st.chat_message("assistant"):
        # stream=True వాడటం వల్ల టెక్స్ట్ వెంటనే ప్రింట్ అవుతుంది
        result = get_ai_response(user_input, combined_info, st.session_state.history)
        st.markdown(result)
        autoplay_audio(result)
            
    st.session_state.messages.append({"role": "assistant", "content": result})
    st.session_state.history += f"Salesperson: {user_input}\nStudent: {result}\n"
    # st.rerun()  <-- దీన్ని కచ్చితంగా తీసేయ్! ఇది ఉన్నంత వరకు నీ యాప్ లాగ్ అవుతూనే ఉంటుంది.


# End Session Logic
st.divider()
if st.button("End Session & Get Performance Report"):
    st.session_state.final_report = get_final_feedback(st.session_state.history)
    st.rerun()

if "final_report" in st.session_state:
    st.markdown("### 📋 Final Sales Performance Report")
    st.write(st.session_state.final_report)
    if st.button("Start New Conversation"):
        st.session_state.messages = []
        st.session_state.history = ""
        del st.session_state.final_report
        st.rerun()

