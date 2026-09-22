from openai import OpenAI 

import time 

# Client used to transcribe
client = OpenAI(
    base_url = "http://localhost:8000/v1",
    api_key="dummy"
)
# Actual transcription api call
def transcribe(audio_file, req_id):
    start = time.time()

    with open(audio_file, "rb") as f:
        result = client.audio.transcriptions.create(
            model="openai/whisper-small",
            file=f,
            language="en"
        )
    latency = time.time() - start 

    return{
        "request": req_id,
        "latency": latency,
        "text_len": len(result.text)
    }
