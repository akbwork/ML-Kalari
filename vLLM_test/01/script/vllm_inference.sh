#!/usr/bin/env bash
set -euo pipefail

# This script's own folder: .../ML-Kalari/vLLM_test/01/script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Go up 3 levels to reach the ML-Kalari project root
KALARI_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

MODEL_DIR="${KALARI_ROOT}/model_repo/openai_whisper-small"
LOG_DIR="${SCRIPT_DIR}/logs"
LOG_FILE="${LOG_DIR}/vllm_audio.log"
HOST="0.0.0.0"
PORT="8000"
# MAX_MODEL_LEN="8192"

mkdir -p "${LOG_DIR}"

echo "Script dir:  ${SCRIPT_DIR}"
echo "Kalari root: ${KALARI_ROOT}"
echo "Model dir:   ${MODEL_DIR}"
echo "Starting vLLM-MLX server... logging to ${LOG_FILE}"

vllm-mlx serve "${MODEL_DIR}" \
    --host "${HOST}" \
    --port "${PORT}" \
    # --max-model-len "${MAX_MODEL_LEN}" \
    --offline \
    2>&1 | tee "${LOG_FILE}"