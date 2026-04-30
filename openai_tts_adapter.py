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

@app.post("/v1/audio/speech")
async def tts(request: Request):
    try:
        data = await request.json()

        logging.info(f"Incoming request JSON: {data}")
        
        text = data.get("input", "")
        
        r = requests.post(
            PIPER_URL,
            json={"text": text}
        )

        logging.info(f"Piper status: {r.status_code}")

        return Response(content=r.content, media_type="audio/wav")
    except Exception as e:
        logging.error(f"Error: {e}", exc_info=True)
        return Response(content=str(e), status_code=500)
