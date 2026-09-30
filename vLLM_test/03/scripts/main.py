import asyncio
import csv
import time
import wave
from pathlib import Path


from client import probe_server
from config import (
    AUDIO_FILES_FOLDER,
    vLLM_BASE_URL,
    CONCURRENCY_LEVELS,
    REQUESTS_PER_USER,
)
from load_generator import LoadGenerator

CSV_HEADER = ["request", "user", "audio_file", "latency", "text_len", "error"]


def load_audio_files(folder: str) -> list[str]:
    candidates = sorted(Path(folder).glob("*.wav"))
    valid = []
    for path in candidates:
        try:
            with wave.open(str(path), "rb") as w:
                w.getnframes()
            valid.append(str(path))
        except Exception:
            print(f"  skipping invalid .wav: {path.name}")
    if not valid:
        raise SystemExit(f"No playable .wav files in {folder}")
    return valid

def percentile(sorted_values: list[float], p: float) -> float:
    if not sorted_values:
        return float("nan")
    k = (len(sorted_values) - 1) * p / 100
    lo = int(k)
    hi = min(lo + 1, len(sorted_values) - 1)
    return sorted_values[lo] if lo == hi else sorted_values[lo] + (sorted_values[hi] - sorted_values[lo]) * (k - lo)


def aggregate(records: list[dict], level: int, wall_time: float) -> dict:
    latencies = sorted(r["latency"] for r in records if not r["error"])
    n = len(records)
    errors = sum(1 for r in records if r["error"])
    return {
        "concurrency": level,
        "requests": n,
        "requests_per_user": REQUESTS_PER_USER,
        "wall_time_s": round(wall_time, 3),
        "throughput_req_s": round(n / wall_time, 3) if wall_time else float("nan"),
        "avg_latency_s": round(sum(latencies) / len(latencies), 3) if latencies else float("nan"),
        "p50_s": round(percentile(latencies, 50), 3) if latencies else float("nan"),
        "p95_s": round(percentile(latencies, 95), 3) if latencies else float("nan"),
        "p99_s": round(percentile(latencies, 99), 3) if latencies else float("nan"),
        "errors": errors,
        "error_rate": round(errors / n, 4) if n else 0.0,
    }


async def main() -> None:
    model = await probe_server()
    audio_files = load_audio_files(AUDIO_FILES_FOLDER)
    print(f"server : {vLLM_BASE_URL}")
    print(f"pool   : {len(audio_files)} audio files\n")

    generator = LoadGenerator(model, audio_files)

    print(f"[sequential] 1 user, {len(audio_files)} files in order")
    start = time.perf_counter()
    seq = await generator.run_sequential()
    seq_row = aggregate(seq, 1, time.perf_counter() - start)
    print(f"  avg={seq_row['avg_latency_s']}s  p95={seq_row['p95_s']}s  errors={seq_row['errors']}\n")

    summary = []
    for level in CONCURRENCY_LEVELS:
        print(f"[concurrent] level={level}  requests={level * REQUESTS_PER_USER}")
        start = time.perf_counter()
        records = await generator.run_concurrent(level)
        row = aggregate(records, level, time.perf_counter() - start)
        summary.append(row)
        print(
            f"  req/s={row['throughput_req_s']}  avg={row['avg_latency_s']}s  "
            f"p50={row['p50_s']}s  p95={row['p95_s']}s  p99={row['p99_s']}s  "
            f"errors={row['errors']} ({row['error_rate']:.2%})"
        )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        raise SystemExit(130)