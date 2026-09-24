# ML-Kalari

Load testing for a Whisper transcription model served with **vLLM**. The test sends audio files at increasing concurrency and records latency and GPU usage.

## Folder Structure

```
ML-Kalari/
├── client/
│   └── transcription.py        # Sends audio to the vLLM server
├── load/
│   └── load_generator.py       # Generates concurrent load
├── gpulogs/
│   └── gpu.csv                 # GPU usage log (nvidia-smi)
├── model_repo/
│   ├── openai_whisper-small/
│   └── taphuynh_whisper_turbo_radiology_en_03_sept/
├── testfiles/                  # Test audio files
├── utils/
│   ├── download_model.py       # Downloads models into model_repo
│   ├── plot.py                 # Plots latency vs users
│   └── latency_vs_users.png
├── vLLM_test/
│   ├── 01/script/
│   │   ├── vllm_inference.sh   # Starts the vLLM server
│   │   └── logs/vllm_audio.log # Server logs
│   └── test.md
├── .env.example
├── config.py
├── main.py                     # Entry point for the load test
├── pyproject.toml
└── Readme.md
```

## Prerequisites

- NVIDIA GPU with the NVIDIA HPC SDK / CUDA runtime installed
- Python environment with vLLM and OpenAI packages

```bash
pip install -U "vllm[audio]" openai
```

## Setup

### 1. CUDA paths (add to `~/.bashrc`)

vLLM must be able to find the NVIDIA HPC toolkit and runtime. On my local machine it is at `/opt/nvidia/hpc_sdk/Linux_x86_64`.

```bash
export CUDA_HOME=/opt/nvidia/hpc_sdk/Linux_x86_64/24.9/cuda
export PATH=/opt/nvidia/hpc_sdk/Linux_x86_64/24.9/compilers/bin:$PATH
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=/opt/nvidia/hpc_sdk/Linux_x86_64/24.9/cuda/12.6/targets/x86_64-linux/lib:$LD_LIBRARY_PATH
```

> **Skipped on the server.** vLLM and CUDA paths were already configured for other projects on the server, and changing them could cause conflicts.

### 2. Environment variables

Copy `.env.example` to `.env` and fill in the values:

```env
MODEL_STORE="/ML-Kalari/model_repo"
MODEL_NAMES="taphuynh/whisper_turbo_radiology_en_03_sept"
HF_TOKEN=""
```

### 3. Test data and logs

- Place test audio files in `testfiles/`
- Logs are written to `vLLM_test/01/script/logs/` (server) and `gpulogs/` (GPU)

## vLLM Deployment

vLLM is deployed on bare-metal servers (ArcaAI AI/ML node).

Start the server (in a separate terminal):

```bash
bash vLLM_test/01/script/vllm_inference.sh
```

Server configuration:

| Setting | Value |
|---|---|
| Model | `taphuynh/whisper_turbo_radiology_en_03_sept` |
| Model path | `model_repo/taphuynh_whisper_turbo_radiology_en_03_sept` |
| Host / Port | `0.0.0.0` / `8015` |
| GPU memory utilization | `0.95` |
| Log file | `vLLM_test/01/script/logs/vllm_audio.log` |

**Quick sanity check with a small model** (optional):

```bash
vllm serve openai/whisper-small --port 8000 2>&1 | tee logs/vllm_audio.log
```

### Verify the server

In a separate terminal:

```bash
curl http://localhost:8015/v1/models
```

The response should list the served model, for example:

```json
{"object":"list","data":[{"id":"taphuynh/whisper_turbo_radiology_en_03_sept","object":"model","owned_by":"vllm", ...}]}
```

## Running the Load Test

Use a separate terminal for each step.

**1. Start GPU monitoring**

```bash
nvidia-smi --query-gpu=timestamp,utilization.gpu,utilization.memory,memory.used,memory.total,power.draw \
  --format=csv -lms 200 > gpulogs/gpu.csv
```

- Adjust `-lms` (sampling interval in ms) to the load so short GPU spikes are not missed.
- This should produce a `gpu.csv` file with entries showing GPU activity.

**2. Run the load test**

```bash
python3 main.py
```

Sample output:

```
Concurrency=1,Avg Latency=0.56s
Concurrency=2,Avg Latency=0.70s
```

**3. (Optional) Plot results**

```bash
python3 utils/plot.py
```

## Expected Outputs

| Output | Description |
|---|---|
| `vLLM_test/01/script/logs/vllm_audio.log` | vLLM server startup and request logs |
| `gpulogs/gpu.csv` | GPU utilization, memory, and power over time |
| Terminal output | Concurrency level and average latency |