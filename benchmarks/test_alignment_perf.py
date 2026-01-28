"""
Benchmark: Memory Alignment Performance (128-bit/16-byte)
Simulates hardware coalescing penalty.
"""
import numpy as np
import time
from utils.hpc_utils import HPCUtils

def benchmark_alignment(iterations: int = 1000):
    size = 1024 * 1024 * 10 # 10MB
    
    # 1. Aligned Buffer
    aligned_buf = HPCUtils.align_buffer(size, alignment=16).copy()
    
    # 2. Unaligned Buffer (1-byte offset)
    raw_data = np.zeros(size + 1, dtype=np.uint8)
    unaligned_buf = raw_data[1:]
    
    print(f"[BENCHMARK] Size: {size/1e6:.1f} MB | Iterations: {iterations}")

    # Test Aligned Path
    start = time.perf_counter()
    for _ in range(iterations):
        # Simulated vectorized operation (summing 128-bit chunks)
        _ = np.sum(aligned_buf.view(np.uint64))
    end = time.perf_counter()
    aligned_time = end - start
    print(f"Aligned Access Time:   {aligned_time:.4f}s")

    # Test Unaligned Path
    start = time.perf_counter()
    for _ in range(iterations):
        _ = np.sum(unaligned_buf.view(np.uint64))
    end = time.perf_counter()
    unaligned_time = end - start
    print(f"Unaligned Access Time: {unaligned_time:.4f}s")
    
    speedup = unaligned_time / aligned_time
    print(f"Speedup Factor:        {speedup:.2f}x")
    print(f"Outcome: {'SUCCESS' if speedup > 1.0 else 'NEUTRAL'} (Higher is better for Aligned)")

if __name__ == "__main__":
    benchmark_alignment()
