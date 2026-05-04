from fastapi import FastAPI, Request, Response
import logging
import requests
import sys

app = FastAPI()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

PIPER_URL = "http://piper:5000"

# 🔊 Voice mapping
VOICE_MAP = {
    "tts-1": "en_US-lessac-medium",   # default
    "lessac": "en_US-lessac-medium",
    "amy": "en_US-amy-medium",
    "british": "en_GB-northern_english_male-medium",
    "joe": "en_US-joe-medium",
    "norman": "en_US-norman-medium",
}


DEFAULT_VOICE = "en_US-lessac-medium"

AVAILABLE_VOICES = set(VOICE_MAP.values())

@app.post("/v1/audio/speech")
async def tts(request: Request):
    try:
        data = await request.json()

        logging.info(f"Incoming request JSON: {data}")
        

        text = data.get("input", "") or " "
        # model = data.get("model", "tts-1")
        voice_input = data.get("voice", "").strip()
        
        # Map model → voice
        voice = VOICE_MAP.get(voice_input, voice_input)

        if voice not in AVAILABLE_VOICES:
            logging.warning(f"Unknown voice '{voice}', falling back")
            voice = DEFAULT_VOICE

        logging.info(f"Using voice: {voice}")

        r = requests.post(
            PIPER_URL,
            json={
                "text": text,
                "voice": voice
            },
            timeout=30
        )


        logging.info(f"Piper status: {r.status_code}")

        return Response(content=r.content, media_type="audio/wav")
    except Exception as e:
        logging.error(f"Error: {e}", exc_info=True)
        return Response(content=str(e), status_code=500)

# 🔍 Optional: list available mappings
@app.get("/v1/voices")
def list_voices():
    return {
        "available_models": list(VOICE_MAP.keys()),
        "default": DEFAULT_VOICE
    }