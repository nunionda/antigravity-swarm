"""
Performance Benchmark for Claude Swarm
"""
import time
from core.manager import SwarmManager
from utils.hpc_utils import HPCUtils

def run_benchmark(swarm_size: int, task_count: int):
    print(f"--- BENCHMARK: SwarmSize={swarm_size}, Tasks={task_count} ---")
    swarm = SwarmManager(swarm_size=swarm_size)
    tasks = [{"id": i, "name": f"T_{i}", "complexity": 1} for i in range(task_count)]
    
    start_time = time.perf_counter()
    results = swarm.dispatch_batch(tasks)
    end_time = time.perf_counter()
    
    total_time = end_time - start_time
    throughput = len(results) / total_time
    
    print(f"Total Time: {total_time:.4f}s")
    print(f"Throughput: {throughput:.2f} tasks/sec")
    print(f"Avg Latency: {(total_time / len(results)) * 1000:.4f}ms")
    
    swarm.shutdown()
    print("--- BENCHMARK COMPLETE ---")

if __name__ == "__main__":
    # Test with varying swarm sizes
    run_benchmark(swarm_size=4, task_count=100)
    run_benchmark(swarm_size=8, task_count=100)
