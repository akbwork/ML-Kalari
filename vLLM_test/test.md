## Steps skipped during testing in Server 


-> Ensure that the nvida HPC toolkit and runtime is installed and where vLLM can find them. In my local machine it is at /opt/nvidia/hpc_sdk/Linux_x86_64

-> Set the following paths (bashrc)

-> export CUDA_HOME=/opt/nvidia/hpc_sdk/Linux_x86_64/24.9/cuda
-> export PATH=/opt/nvidia/hpc_sdk/Linux_x86_64/24.9/compilers/bin:$PATH
-> export PATH=$CUDA_HOME/bin:$PATH
-> Export the LD library path (bashrc): export LD_LIBRARY_PATH=/opt/nvidia/hpc_sdk/Linux_x86_64/24.9/cuda/12.6/targets/x86_64-linux/lib:$LD_LIBRARY_PATH

### Reason for Skipping -
1. vLLM and CUDA paths are already set for other projects in server
2. Changing the Paths might create conflict with other projects


## vLLM Deployment Details

- vLLM is deployed in Bare-metal servers, ArcaAi Ai/ML node


## vLLM Curl Commands


## NSight Commands
1. Python Script: 
    - nsys profile   --trace=cuda,nvtx,osrt,cudnn,cublas   --sample=cpu   --python-sampling=true   -o report uv run main.py

2. vLLM:
    - nsys profile \
  --trace=cuda,nvtx,osrt \
  --trace-fork-before-exec=true \
  --cuda-graph-trace=node \
  --delay=30 --duration=30 \
  -o vllm_report --force-overwrite=true \
  bash vLLM_test/02/script/vllm_nsight_inference.sh

