import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

vLLM_BASE_URL = os.getenv(key="vLLM_BASE_URL")

AUDIO_FILES_FOLDER = "/Users/ananthakrishnab/Desktop/Projects/vLLM Serving/ML-Kalari/testfiles"

REQUESTS_PER_USER = 12

CONCURRENCY_LEVELS = [
    1,
    2,
    4,
    8,
    16,
    32,
    64,
    128,
    256,
    512,
    1024
]