from openai import OpenAI 
from config import CHUNK_SIZE

import time 
import wave

# Client used to transcribe
client = OpenAI(
    base_url = "http://localhost:8015/v1",
    api_key="dummy",
    timeout=60.0,
    max_retries=2,
)

MODEL_ID = client.models.list().data[0].id

def transcribe(audio_file, req_id):
    start = time.time()

    try:
        with open(audio_file, "rb") as f:
            result = client.audio.transcriptions.create(
                model=MODEL_ID,
                file=f,
                language="en",
                # stream=True,
                response_format="verbose_json",
                timestamp_granularities=["segment"],
            )
        latency = time.time() - start 

        print("*********************")
        print(result)
        print("*********************")

        return{
            "request": req_id,
            "latency": latency,
            "text_len": len(result.text),
            "text": result.text,
            "input_duration": result.duration,
            "usage": result.usage,
            "metrics": result.model_extra.get("metrics"),
        }
    except Exception as e:
        return {
            "request": req_id,
            "latency": time.time() - start,
            "text_len": None,
            "error": str(e)
        }

def get_audio_duration(audio_file):
    try:
        with wave.open(f=audio_file, mode="rb") as audio:
            frames = audio.getnframes()
            sample_rate = audio.getframerate()

        duration = frames / sample_rate
        return duration
    except Exception as e:
        print(f"Failed to get audio duration - {e}")
        return None



if __name__ == "__main__":
    AUDIO_FILE = "/Users/ananthakrishnab/Desktop/Projects/vLLM Serving/ML-Kalari/testfiles/YT_download.wav"

    duration = get_audio_duration(audio_file=AUDIO_FILE)
    if duration is not None:
        print(f"Duration of the audio - {duration:.2f} seconds")

    response = transcribe(audio_file=AUDIO_FILE, req_id=1)
    print(response)

