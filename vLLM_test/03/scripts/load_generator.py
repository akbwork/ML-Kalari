from concurrent.futures import ThreadPoolExecutor

"""
12 Audio Files ->
1 -> 1024 Concurrent Users

Single Request (Sequential)
User 1 -> Send Audio 1, Send Audio 2, Send Audio 3....Audio 12

Concurrent Request
User 1 -> Send Random Audio from Audio Files
User 2 -> Send Random Audio from Audio Files

Concurrent Request
User 1 -> Send Random Audio from Audio Files
User 2 -> Send Random Audio from Audio Files
User 3 -> Send Random Audio from Audio Files
User 4 -> Send Random Audio from Audio Files

"""

import asyncio
import itertools
import random

from client import transcribe
from config import REQUESTS_PER_USER


class LoadGenerator:
    def __init__(self, model: str, audio_files: list[str]):
        self.model = model
        self.audio_files = list(audio_files)

    async def run_sequential(self) -> list[dict]:
        req_ids = itertools.count(1)
        return [
            await transcribe(audio_file, next(req_ids), user_id=0, model=self.model)
            for audio_file in self.audio_files
        ]

    async def run_concurrent(self, concurrency: int) -> list[dict]:
        semaphore = asyncio.Semaphore(concurrency)
        req_ids = itertools.count(1)

        async def worker(user_id: int) -> list[dict]:
            local = []
            for _ in range(REQUESTS_PER_USER):
                audio_file = random.choice(self.audio_files)
                async with semaphore:  # true "level" in-flight, no 1024 threads
                    local.append(
                        await transcribe(audio_file, next(req_ids), user_id, self.model)
                    )
            return local

        batches = await asyncio.gather(*(worker(u) for u in range(concurrency)))
        return [r for batch in batches for r in batch]