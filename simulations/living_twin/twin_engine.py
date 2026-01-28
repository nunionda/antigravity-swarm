"""
LivingTwin: Twin Engine
Hyperscale orchestrator for 100,000 agent digital twin.
"""
import numpy as np
from core.manager import SwarmManager
from simulations.living_twin.agent_dynamics import DynamicsKernel
from simulations.living_twin.twin_visualizer import TwinVisualizer
from utils.hpc_utils import HPCUtils

class LivingTwinEngine:
    def __init__(self, agent_count: int = 100000):
        self.agent_count = agent_count
        self.swarm = SwarmManager(swarm_size=32, worker_class=DynamicsKernel)
        self.visualizer = TwinVisualizer()
        # Step 02: PINNED_HOST_MEMORY allocation for 100k agent states (simulated)
        # Using numpy for vectorized alignment and speed
        initial_pos = np.random.rand(agent_count, 2).astype(np.float32) * 2000
        # Snap to grid: Major roads every 300 units
        for i in range(agent_count):
            if i % 2 == 0: # Snap to vertical road
                initial_pos[i, 0] = (initial_pos[i, 0] // 300) * 300
            else: # Snap to horizontal road
                initial_pos[i, 1] = (initial_pos[i, 1] // 300) * 300
                
        self.state_pool = {
            "pos": initial_pos,
            "wealth": np.random.rand(agent_count, 1).astype(np.float32),
            "speed": np.zeros(agent_count, dtype=np.float32),
            "type": np.array([1 if i % 5 == 0 else 0 for i in range(agent_count)], dtype=np.int32),
            "status": np.zeros(agent_count, dtype=np.int32)
        }
        print(f"🏙️ [TWIN] City Initialized: {agent_count:,} agents in Pinned Memory.")

    @HPCUtils.benchmark_latency
    def update_world(self, iteration: int):
        """
        Executes a global update cycle for all 100,000 agents.
        """
        batch_size = 2000
        tasks = []
        for i in range(0, self.agent_count, batch_size):
            tasks.append({
                "id": f"iter_{iteration}_batch_{i}",
                "range": (i, min(i + batch_size, self.agent_count)),
                "pressure": -0.05, # Slight economic contraction
                "complexity": 1
            })
            
        # Dispatch 100,000 agents in 50 batches to the 32-worker swarm
        results = self.swarm.dispatch_batch(tasks)
        
        # Step 05: STREAMING write-back to the state pool
        # In a real engine, we'd use non-temporal stores here
        for r in results:
            for agent_res in r['batch_results']:
                idx = agent_res['id']
                self.state_pool["pos"][idx] += agent_res['pos_delta']
                self.state_pool["wealth"][idx] += agent_res['wealth_delta']
                self.state_pool["speed"][idx] = agent_res['speed']
                
        # Phase 3: Visual Export
        avg_speed = float(np.mean(self.state_pool["speed"]))
        # Step 05: Visual Snapshot Generation
        snapshot = self.visualizer.generate_snapshot(self.state_pool)
        snapshot["avg_speed"] = avg_speed
        self.visualizer.save_snapshot(snapshot, "apps/living_twin_dashboard/snapshot.json")
                
        return len(results)

    def shutdown(self):
        self.swarm.shutdown()

if __name__ == "__main__":
    engine = LivingTwinEngine(agent_count=100000)
    engine.update_world(1)
    engine.shutdown()
