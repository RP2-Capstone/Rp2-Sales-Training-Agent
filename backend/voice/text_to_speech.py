from gtts import gTTS
from pathlib import Path
import uuid
import re
from config import (
    VOICE_ENABLED,
    VOICE_LANGUAGE,
    VOICE_SPEED
)


AUDIO_DIR       = Path("audio")
MAX_TEXT_LENGTH = 300     # characters
MAX_FILES_KEPT  = 20      # old files to keep


def clean_text(text: str) -> str:
    """
    Remove markdown and special characters
    that sound bad when spoken out loud

    Example:
    "**Hello** - this is _great_!"
    becomes:
    "Hello this is great!"
    """

    # ✅ Remove bold markdown  **text**
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)

    # ✅ Remove italic markdown  _text_ or *text*
    text = re.sub(r'[_*](.*?)[_*]', r'\1', text)

    # ✅ Remove bullet points  - item  or  • item
    text = re.sub(r'^\s*[-•]\s+', '', text, flags=re.MULTILINE)

    # ✅ Remove numbered lists  1. item  2. item
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)

    # ✅ Remove hashtag headers  # Heading
    text = re.sub(r'#+ ', '', text)

    # ✅ Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def trim_text(text: str, max_length: int = MAX_TEXT_LENGTH) -> str:
    """
    Cut text at sentence boundary
    so audio doesn't end mid-sentence

    Example (max 50 chars):
    "Hello there. This is a very long sentence that goes on."
    becomes:
    "Hello there."
    """
    if len(text) <= max_length:
        return text

    # ✅ Cut at last full sentence within limit
    trimmed = text[:max_length].rsplit('.', 1)[0]

    # ✅ Add period if missing
    if not trimmed.endswith('.'):
        trimmed += '.'

    return trimmed



def cleanup_old_files():
    """
    Keep only the latest MAX_FILES_KEPT audio files
    Delete the rest to save disk space
    """
    files = sorted(
        AUDIO_DIR.glob("*.mp3"),
        key=lambda f: f.stat().st_mtime     # sort by modified time
    )

    # ✅ If more than limit → delete oldest
    if len(files) > MAX_FILES_KEPT:
        for old_file in files[:-MAX_FILES_KEPT]:
            old_file.unlink()
            print(f"🗑️ Deleted old audio: {old_file.name}")


def convert_text_to_speech(text: str):
    """
    Convert text to speech and save as mp3

    Returns:
        filename (str) if successful
        None if failed or voice disabled
    """

    # ✅ Check if voice is enabled in config
    if not VOICE_ENABLED:
        print("🔇 Voice disabled in config")
        return None

    # ✅ Check empty text
    if not text or not text.strip():
        print("⚠️ Empty text passed to TTS")
        return None

    try:
        # ✅ Create audio folder if not exists
        AUDIO_DIR.mkdir(exist_ok=True)

        # ✅ Clean markdown from text
        text = clean_text(text)

        # ✅ Trim to max length at sentence boundary
        text = trim_text(text)

        print(f"🔊 Converting to speech: {text[:50]}...")

        # ✅ Generate unique filename
        filename = f"response_{uuid.uuid4().hex}.mp3"
        filepath = AUDIO_DIR / filename

        # ✅ Generate audio using config settings
        tts = gTTS(
            text=text,
            lang=VOICE_LANGUAGE,    # from config.py
            slow=VOICE_SPEED        # from config.py
        )
        tts.save(str(filepath))

        # ✅ Clean old files after saving
        cleanup_old_files()

        print(f"✅ Audio saved: {filename}")
        return filename

    except Exception as e:
        print(f"❌ TTS Error: {e}")
        return None