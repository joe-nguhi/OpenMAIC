FROM python:3.11-slim

WORKDIR /app

RUN pip install fastapi uvicorn requests

COPY openai_tts_adapter.py .

CMD ["uvicorn", "openai_tts_adapter:app", "--host", "0.0.0.0", "--port", "8000"]