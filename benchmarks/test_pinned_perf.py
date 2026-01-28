"""
Benchmark: Pinned Memory Transfer Efficiency
Simulates DMA/Transfer performance.
"""
import numpy as np
import time
from utils.hpc_utils import HPCUtils

def benchmark_pinned_memory(size_mb: int = 50):
    size = size_mb * 1024 * 1024
    iterations = 100
    
    print(f"[BENCHMARK] Data Size: {size_mb} MB | Iterations: {iterations}")

    # 1. Standard Pageable Memory (Simulated via normal np array)
    standard_data = np.random.bytes(size)
    
    # 2. Pinned Memory (HPCUtils strategy)
    pinned_view = HPCUtils.get_pinned_memory(size)
    pinned_view[:] = standard_data # Initial fill
    
    # Transfer Test (Target is another buffer)
    target = bytearray(size)

    # Standard Transfer
    start = time.perf_counter()
    for _ in range(iterations):
        target[:] = standard_data
    end = time.perf_counter()
    standard_time = end - start
    print(f"Standard Memory Transfer: {standard_time:.4f}s")

    # Pinned Transfer (Simulated DMA-optimized path)
    start = time.perf_counter()
    for _ in range(iterations):
        # Pinned memory views are faster in memory-to-memory copies in many runtimes
        # as they provide direct contiguous access without extra internal checks
        target[:] = pinned_view
    end = time.perf_counter()
    pinned_time = end - start
    print(f"Pinned Memory Transfer:   {pinned_time:.4f}s")
    
    speedup = standard_time / pinned_time
    print(f"Speedup Factor:          {speedup:.2f}x")

if __name__ == "__main__":
    benchmark_pinned_memory()
