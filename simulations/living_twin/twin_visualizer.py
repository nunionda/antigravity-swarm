"""
LivingTwin: Visualizer
Exports agent state snapshots for real-time visualization.
"""
import json
import time
import numpy as np

class TwinVisualizer:
    @staticmethod
    def generate_snapshot(state_pool: dict, sample_size: int = 10000):
        """
        Exports a representative sample of 100k agents for visualization.
        """
        indices = np.random.choice(len(state_pool["pos"]), sample_size, replace=False)
        positions = state_pool["pos"][indices].tolist()
        types = state_pool["type"][indices].tolist()
        
        payload = {
            "timestamp": time.time(),
            "agents": [
                {"x": p[0], "y": p[1], "t": t} 
                for p, t in zip(positions, types)
            ]
        }
        return payload

    @staticmethod
    def save_snapshot(payload: dict, file_path: str):
        with open(file_path, 'w') as f:
            json.dump(payload, f)
        # print(f"📸 [VISUALIZER] Snapshot saved to {file_path}")
import time
