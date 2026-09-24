# AUDIO_FILE = "/data/arcaai/ananth/projects/Github/ML-Kalari/testfiles/DannyBCM002_CTChestPlainContrast_Acute.wav"

AUDIO_PATH = "/data/arcaai/ananth/projects/Github/ML-Kalari/testfiles/DannyBCM002_CTChestPlainContrast_Acute.wav"

with open(AUDIO_PATH, "rb") as f:   # "rb" = binary mode
    AUDIO_FILE = f.read()

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