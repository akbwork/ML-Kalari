# To access threads
from concurrent.futures import ThreadPoolExecutor
# To acess results from each thread without waiting for the other threads
from concurrent.futures import as_completed 
# Custom transcription pay load
from client.transcription import transcribe 

"""Central object that will control the load testing"""
class LoadGenerator:
    def __init__(self, audio_file):
        self.audio_file = audio_file 

    def run(self, concurrency):
        results = []
        with ThreadPoolExecutor(
            max_workers = concurrency # creates threads = 1, 2, 4, 8, 16 on each independent run
        )as executor:
            
            # All future handles are stored here from executor returns
            futures = [
                executor.submit(
                    transcribe, # job 
                    self.audio_file, # data
                    i # no of threads executing it independently
                )
                for i in range(concurrency)
            ]
            # As threads finish executing, store the results from their future into the results. 
            # This should contain: request id, latency and text_len 
            for future in as_completed(futures):
                results.append(
                    future.result()
                )

        return results

