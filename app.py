
import streamlit as st
from streamlit_mic_recorder import speech_to_text
from services.api_client import get_ai_response, get_final_feedback
from frontend_logic.persona_config import PERSONAS, COURSES

# Page Config
st.set_page_config(page_title="RP2 AI Sales Trainer", layout="wide", page_icon="🛡️")

# Session State Initialization
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

# --- UI Layout: Chat Messages ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- INPUT HANDLING: Chat Box + Mic Next to it ---
# ఇక్కడ మనం కాలమ్స్ వాడుతున్నాము (చాట్ బాక్స్ 90% + మైక్ 10%)
col1, col2 = st.columns([0.9, 0.1])

with col1:
    prompt = st.chat_input("Type your pitch here...")

with col2:
    # మైక్ బటన్ ని ఇక్కడ పెట్టాము
    audio_text = speech_to_text(key=f"mic_{st.session_state.mic_counter}", use_container_width=True)

user_input = None
if prompt:
    user_input = prompt
elif audio_text:
    user_input = audio_text
    st.session_state.mic_counter += 1

# Process Input
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    combined_info = {**PERSONAS[selected_p_name], "name": selected_p_name, "course": selected_course}
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = get_ai_response(user_input, combined_info, st.session_state.history)
            st.markdown(result)
            
    st.session_state.messages.append({"role": "assistant", "content": result})
    st.session_state.history += f"Salesperson: {user_input}\nStudent: {result}\n"
    st.rerun()

# --- End Session Logic ---
st.divider()
if st.button("End Session & Get Performance Report"):
    with st.spinner("Generating professional feedback..."):
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