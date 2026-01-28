"""
Omni-Scribe Impact Analyzer
Orchestrates a swarm to propagate changes through the dependency graph.
"""
from core.manager import SwarmManager
from engine.context_bus import ContextBus
from utils.hpc_utils import HPCUtils

class ImpactAnalyzer:
    def __init__(self, bus: ContextBus):
        self.bus = bus
        self.swarm = SwarmManager(swarm_size=8)
        print("[OMNI-SCRIBE] ImpactAnalyzer initialized with 8-worker Swarm.")

    @HPCUtils.benchmark_latency
    def analyze_change(self, modified_file: str):
        """
        Determines the global impact of a change in 'modified_file'.
        Dispatches analysis tasks to the swarm in parallel.
        """
        context = self.bus.get_context()
        impacted_files = []
        
        # Simulate dependency discovery
        # In production, this reads the pre-calculated dependency graph from memory
        tasks = []
        for file_path, ast_summary in context.items():
            if file_path != modified_file:
                tasks.append({
                    "id": file_path,
                    "name": f"Audit_{file_path}",
                    "complexity": 1,
                    "target": modified_file
                })
        
        print(f"[OMNI-SCRIBE] Dispatching {len(tasks)} impact audits to swarm...")
        results = self.swarm.dispatch_batch(tasks)
        return [r['worker_id'] for r in results if r['status'] == 'COMPLETED']

    def shutdown(self):
        self.swarm.shutdown()

if __name__ == "__main__":
    bus = ContextBus()
    # Mock some project context
    for i in range(100):
        bus.update_file_state(f"module_{i}.py", {"functions": ["foo"]})
        
    analyzer = ImpactAnalyzer(bus)
    analyzer.analyze_change("core_lib.py")
    analyzer.shutdown()
