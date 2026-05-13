from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path

router = APIRouter()


class TTSRequest(BaseModel):
    text: str


@router.post("/tts")
def text_to_speech(request: TTSRequest):
    try:
        from voice.text_to_speech import convert_text_to_speech

        if not request.text or not request.text.strip():
            return {"error": "Text cannot be empty"}

        filename = convert_text_to_speech(request.text)

        if not filename:
            return {"error": "TTS failed or voice is disabled"}

        return {
            "filename": filename,
            "audio_url": f"/voice/audio/{filename}"
        }

    except Exception as e:
        print("TTS Error:", e)
        return {"error": "Something went wrong in TTS"}


@router.get("/audio/{filename}")
def get_audio(filename: str):
    try:
        if not filename.endswith(".mp3"):
            raise HTTPException(
                status_code=400,
                detail="Only .mp3 files allowed"
            )

        if ".." in filename or "/" in filename:
            raise HTTPException(
                status_code=400,
                detail="Invalid filename"
            )

        audio_dir = Path("audio").resolve()
        file_path = (audio_dir / filename).resolve()

        if not str(file_path).startswith(str(audio_dir)):
            raise HTTPException(
                status_code=400,
                detail="Access denied"
            )

        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail="Audio file not found"
            )

        return FileResponse(
            path=file_path,
            media_type="audio/mpeg",
            filename=filename
        )

    except HTTPException:
        raise

    except Exception as e:
        print("Audio Error:", e)
        raise HTTPException(
            status_code=500,
            detail="Something went wrong"
        )