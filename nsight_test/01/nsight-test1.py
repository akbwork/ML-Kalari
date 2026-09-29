import time
import torch

print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())

if not torch.cuda.is_available():
    raise RuntimeError("CUDA is not available")

print("GPU:", torch.cuda.get_device_name(0))


# --------------------------------------------------
# 1. Allocate data
# --------------------------------------------------

N = 4096

print(f"Creating {N}x{N} matrices...")

a = torch.randn(N, N, device="cuda")
b = torch.randn(N, N, device="cuda")


# --------------------------------------------------
# 2. Warm-up
# --------------------------------------------------

print("Warming up GPU...")

for _ in range(10):
    c = torch.matmul(a, b)

torch.cuda.synchronize()


# --------------------------------------------------
# 3. Profiled workload
# --------------------------------------------------

print("Starting workload...")

for i in range(20):

    torch.cuda.nvtx.range_push(f"Iteration {i}")

    # Matrix multiplication
    c = torch.matmul(a, b)

    # Another GPU operation
    d = torch.relu(c)

    # Force CPU to wait for GPU
    torch.cuda.synchronize()

    torch.cuda.nvtx.range_pop()

    time.sleep(0.05)


print("Finished.")

print("Result:", d[0, 0].item())