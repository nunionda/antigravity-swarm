"""
AgentWorker: Individual execution unit in the Claude Swarm
"""
import uuid
import time
from utils.hpc_utils import HPCUtils

class AgentWorker:
    def __init__(self, worker_id: str = None):
        self.worker_id = worker_id or str(uuid.uuid4())[:8]
        self.status = "IDLE"
        self.last_task_latency = 0.0

    @HPCUtils.benchmark_latency
    def execute(self, task: dict) -> dict:
        """
        Executes a task with performance monitoring.
        """
        self.status = "BUSY"
        # Simulate processing time based on task complexity
        complexity = task.get("complexity", 1)
        time.sleep(0.01 * complexity) 
        
        result = {
            "worker_id": self.worker_id,
            "task_id": task.get("id"),
            "status": "COMPLETED",
            "payload": f"Processed {task.get('name')}"
        }
        self.status = "IDLE"
        return result

    def __repr__(self):
        return f"<AgentWorker id={self.worker_id} status={self.status}>"
