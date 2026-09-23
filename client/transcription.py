from openai import OpenAI 

import time 

# Client used to transcribe
client = OpenAI(
    base_url = "http://localhost:8015/v1",
    api_key="dummy",
    timeout=60.0,
    max_retries=2,
)
# Actual transcription api call
def transcribe(audio_bytes: bytes, filename: str, req_id: int):
    start = time.time()

    try:
        # Pass (filename, bytes) tuple instead of file object 'f'
        result = client.audio.transcriptions.create(
            model="openai/whisper-small",
            file=(filename, audio_bytes),
            language="en"
        )
        latency = time.time() - start
        return {
            "request": req_id,
            "latency": latency,
            "text_len": len(result.text),
            "error": None
        }
    except Exception as e:
        return {
            "request": req_id,
            "latency": time.time() - start,
            "text_len": None,
            "error": str(e)
        }
