"""
SwarmManager: Central orchestrator for the Claude Swarm
"""
import concurrent.futures
from typing import List, Dict
from core.worker import AgentWorker
from utils.hpc_utils import HPCUtils

class SwarmManager:
    def __init__(self, swarm_size: int = 4):
        self.workers = [AgentWorker() for _ in range(swarm_size)]
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=swarm_size)
        print(f"[SWARM] Initialized with {swarm_size} workers.")

    @HPCUtils.benchmark_latency
    def dispatch_batch(self, tasks: List[Dict]) -> List[Dict]:
        """
        Dispatches a batch of tasks to workers in parallel.
        Ensures high-throughput by utilizing a pool of workers.
        """
        futures = []
        results = []
        
        # Simple round-robin or first-available assignment via ThreadPoolExecutor
        for i, task in enumerate(tasks):
            worker = self.workers[i % len(self.workers)]
            futures.append(self.executor.submit(worker.execute, task))
            
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
            
        return results

    def shutdown(self):
        self.executor.shutdown()
        print("[SWARM] Shutdown complete.")

if __name__ == "__main__":
    # Quick test
    swarm = SwarmManager(swarm_size=4)
    sample_tasks = [{"id": i, "name": f"Task_{i}", "complexity": 1} for i in range(10)]
    
    print(f"[SWARM] Dispatching {len(sample_tasks)} tasks...")
    results = swarm.dispatch_batch(sample_tasks)
    print(f"[SWARM] Received {len(results)} results.")
    swarm.shutdown()
