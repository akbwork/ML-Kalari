from config import (AUDIO_FILE, CONCURRENCY_LEVELS)

from load.load_generator import(LoadGenerator)

generator = LoadGenerator(AUDIO_FILE)

for concurrency in CONCURRENCY_LEVELS:
    results = generator.run(concurrency)

    # avg_latency = (
    #     sum(r["latency"] for r in results)/ len(results)
    # )

    # print(
    #     f"Concurrency={concurrency},"
    #     f"Avg Latency={avg_latency:.2f}s"
    # )

    successful = [r for r in results if r["latency"] is not None]
    failed_count = len(results) - len(successful)

    if successful:
        avg_latency = sum(r["latency"] for r in successful) / len(successful)
        print(f"Concurrency={concurrency}, Avg Latency={avg_latency:.2f}s, "
            f"Success={len(successful)}/{len(results)}, Failed={failed_count}")
    else:
        print(f"Concurrency={concurrency}, ALL {len(results)} requests failed")