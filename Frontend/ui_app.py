import streamlit as st
from streamlit_mic_recorder import mic_recorder

# Set page title and header
st.title("🎙️ AI Sales Training Agent")
st.subheader("Practice your sales pitch")

# Voice recording section
st.write("Click the microphone button below to start speaking:")

# Recording button logic
audio = mic_recorder(
    start_prompt="Start Recording ⏺️",
    stop_prompt="Stop Recording ⏹️",
    key='recorder'
)

# Process recording
if audio:
    st.audio(audio['bytes'])
    st.success("Voice recorded successfully! Converting to text...")
    
    # Next step: Add logic to send audio['bytes'] to Whisper API or your Backend
