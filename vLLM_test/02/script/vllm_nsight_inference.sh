#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KALARI_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

MODEL_DIR="${KALARI_ROOT}/model_repo/taphuynh_whisper_turbo_radiology_en_03_sept"
LOG_DIR="${SCRIPT_DIR}/logs"
LOG_FILE="${LOG_DIR}/vllm_audio.log"
HOST="0.0.0.0"
PORT="8015"
GPU_MEMORY_UTIL=0.95 # 95% GPU

mkdir -p "${LOG_DIR}"

echo "Script dir:  ${SCRIPT_DIR}"
echo "Kalari root: ${KALARI_ROOT}"
echo "Model dir:   ${MODEL_DIR}"
echo "Starting vLLM-MLX server... logging to ${LOG_FILE}"

vllm serve "${MODEL_DIR}" \
    --host "${HOST}" \
    --port "${PORT}" \
    --gpu-memory-utilization "${GPU_MEMORY_UTIL}" \
    --served-model-name "taphuynh/whisper_turbo_radiology_en_03_sept" \
    --allowed-origins '["*"]' \
    2>&1 | tee "${LOG_FILE}"