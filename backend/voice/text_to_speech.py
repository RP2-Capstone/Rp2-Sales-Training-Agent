from gtts import gTTS
import uuid
from pathlib import Path

def convert_text_to_speech(text):
    try:
        # Limit text length (optional safety)
        text = text[:300]

        # Create audio folder
        audio_dir = Path("audio")
        audio_dir.mkdir(exist_ok=True)

        # Unique filename
        filename = f"response_{uuid.uuid4().hex}.mp3"
        filepath = audio_dir / filename

        # Generate audio
        tts = gTTS(text=text, lang='en')
        tts.save(str(filepath))

        return filename

    except Exception as e:
        print("TTS Error:", e)
        return None
