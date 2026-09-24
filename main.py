from config import (AUDIO_FILE, CONCURRENCY_LEVELS)

from load.load_generator import(LoadGenerator)

generator = LoadGenerator(AUDIO_FILE)

for concurrency in CONCURRENCY_LEVELS:
    results = generator.run(concurrency)

    avg_latency = (
        sum(r["latency"] for r in results)/ len(results)
    )

    print(
        f"Concurrency={concurrency},"
        f"Avg Latency={avg_latency:.2f}s"
    )