
FROM python:3.11-slim

WORKDIR /app

RUN pip install piper-tts[http] && \
    python3 -m piper.download_voices en_US-lessac-medium

CMD ["python3", "-m", "piper.http_server", "-m", "en_US-lessac-medium", "--host", "0.0.0.0", "--port", "5000"]
