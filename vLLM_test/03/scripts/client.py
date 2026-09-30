from openai import OpenAI, AsyncOpenAI
from config import CHUNK_SIZE

import time 
import wave

from config import vLLM_BASE_URL

# Client used to transcribe
# client = OpenAI(
#     base_url = vLLM_BASE_URL,
#     api_key="dummy",
#     timeout=60.0,
#     max_retries=2,
# )

client = AsyncOpenAI(
    base_url = vLLM_BASE_URL,
    api_key="dummy",
    timeout=60.0,
    max_retries=2,
)

# MODEL_ID = client.models.list().data[0].id


async def probe_server() -> str:
    """Fail-fast reachability check; returns the served model id."""
    try:
        models = await client.models.list()
    except Exception as exc:
        raise ConnectionError(
            f" ({exc})"
        ) from exc
    if not models.data:
        raise ConnectionError(f"Server at {vLLM_BASE_URL} reported no models.")
    return models.data[0].id

# def transcribe(audio_file, req_id):
#     start = time.perf_counter()

#     try:
#         with open(audio_file, "rb") as f:
#             result = client.audio.transcriptions.create(
#                 model=MODEL_ID,
#                 file=f,
#                 language="en",
#                 # stream=True,
#                 response_format="verbose_json",
#                 timestamp_granularities=["segment"],
#             )
#         latency = time.perf_counter() - start

#         # print("*********************")
#         # print(result)
#         # print("*********************")

#         return{
#             "request": req_id,
#             "latency": latency,
#             "text_len": len(result.text),
#             "text": result.text,
#             "input_duration": result.duration,
#         }
#     except Exception as e:
#         return {
#             "request": req_id,
#             "latency": time.time() - start,
#             "text_len": None,
#             "error": str(e)
#         }

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


async def transcribe(audio_file: str, req_id: int, user_id: int, model: str) -> dict:
    start = time.perf_counter()
    try:
        with open(audio_file, "rb") as f:
            result = await client.audio.transcriptions.create(
                model=model,
                file=f,
                language="en",
            )
        return {
            "request": req_id,
            "user": user_id,
            "audio_file": audio_file,
            "latency": time.perf_counter() - start,
            "text_len": len(result.text),
            "error": "",
        }
    except Exception as exc:
        return {
            "request": req_id,
            "user": user_id,
            "audio_file": audio_file,
            "latency": time.perf_counter() - start,
            "text_len": None,
            "error": str(exc),
        }


if __name__ == "__main__":
    AUDIO_FILE = "/Users/ananthakrishnab/Desktop/Projects/vLLM Serving/ML-Kalari/testfiles/YT_download.wav"

    duration = get_audio_duration(audio_file=AUDIO_FILE)
    if duration is not None:
        print(f"Duration of the audio - {duration:.2f} seconds")

    response = transcribe(audio_file=AUDIO_FILE, req_id=1)
    print(response)

