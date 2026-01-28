"""
Benchmark: Architecture Scaling (Swarm vs. Sandbox V3)
"""
import time
import asyncio
from core.manager import SwarmManager

# Mocking legacy sequential sandbox behavior (AgentWorkflowV3 style)
class LegacySandbox:
    def __init__(self, size: int):
        self.size = size

    def execute_task(self, task):
        # Simulated isolated process with deep copying overhead
        start = time.perf_counter()
        _ = bytearray(1024 * 1024) # simulated overhead
        time.sleep(0.01) # task processing
        return {"status": "OK"}

    def run_sequential(self, tasks):
        results = []
        for task in tasks:
            results.append(self.execute_task(task))
        return results

def benchmark_scaling():
    task_count = 50
    tasks = [{"id": i} for i in range(task_count)]
    
    print(f"[BENCHMARK] Scaling Comparison | Tasks: {task_count}")

    # 1. Legacy Sandbox (Sequential)
    legacy = LegacySandbox(size=task_count)
    start = time.perf_counter()
    _ = legacy.run_sequential(tasks)
    end = time.perf_counter()
    legacy_time = end - start
    print(f"Legacy Sequential (Sandbox): {legacy_time:.4f}s")

    # 2. Claude Swarm (Parallel Orchestrator)
    swarm = SwarmManager(swarm_size=8)
    start = time.perf_counter()
    _ = swarm.dispatch_batch(tasks)
    end = time.perf_counter()
    swarm_time = end - start
    print(f"Claude Swarm (Parallel):     {swarm_time:.4f}s")
    swarm.shutdown()

    speedup = legacy_time / swarm_time
    print(f"Architecture Speedup:        {speedup:.2f}x")

if __name__ == "__main__":
    benchmark_scaling()
