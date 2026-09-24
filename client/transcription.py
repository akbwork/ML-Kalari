from openai import OpenAI 

import time 

# Client used to transcribe
client = OpenAI(
    base_url = "http://localhost:8015/v1",
    api_key="dummy",
    timeout=60.0,
    max_retries=2,
)

MODEL_ID = client.models.list().data[0].id


# Actual transcription api call
def transcribe(audio_file, req_id):
    start = time.time()

    try:
        with open(audio_file, "rb") as f:
            result = client.audio.transcriptions.create(
                model=MODEL_ID,
                file=f,
                language="en"
            )
        latency = time.time() - start 

        return{
            "request": req_id,
            "latency": latency,
            "text_len": len(result.text)
        }
    except Exception as e:
        return {
            "request": req_id,
            "latency": time.time() - start,
            "text_len": None,
            "error": str(e)
        }