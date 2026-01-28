"""
BioSwarm: Molecular Orchestrator
Manages the folding process of a 10,000 residue protein chain.
"""
import numpy as np
import time
import json
import os
from core.manager import SwarmManager
from simulations.bioswarm.bio_physics import BioPhysicsKernel
from simulations.bioswarm.pdb_parser import PDBParser
from utils.hpc_utils import HPCUtils

class BioSwarmEngine:
    def __init__(self, pdb_path: str = None):
        if pdb_path and os.path.exists(pdb_path):
            atoms = PDBParser.parse_pdb(pdb_path)
            self.positions = np.array([a["pos"] for a in atoms], dtype=np.float32)
            self.ss_list = [a["ss"] for a in atoms]
            self.residue_count = len(self.positions)
            print(f"🧬 [BioSwarm] Loaded PDB {pdb_path}: {self.residue_count} residues.")
        else:
            self.residue_count = 500
            self.positions = np.cumsum(np.random.normal(0, 1.0, (500, 3)), axis=0).astype(np.float32)
            self.ss_list = ["C"] * 500
            print(f"🧬 [BioSwarm] Chain Initialized: 500 residues (Random Coil).")
            
        self.swarm = SwarmManager(swarm_size=32, worker_class=BioPhysicsKernel)
        self.velocities = np.zeros((self.residue_count, 3), dtype=np.float32)
        
        self.config = {
            "dt": 0.01,
            "damping": 0.9,
            "max_force": 100.0,
            "batch_size": 200
        }
        
        # Snapshot directory
        os.makedirs("apps/bioswarm_monitor", exist_ok=True)

    @HPCUtils.benchmark_latency
    def step(self, iteration: int):
        """
        Single MD integration step.
        """
        start_time = time.perf_counter()
        batch_size = self.config["batch_size"]
        tasks = []
        for i in range(0, self.residue_count, batch_size):
            tasks.append({
                "id": f"bio_step_{iteration}_batch_{i}",
                "range": (i, min(i + batch_size, self.residue_count)),
                "positions": self.positions.tolist()
            })
            
        # Dispatch to Swarm
        results = self.swarm.dispatch_batch(tasks)
        
        # Integration
        dt = self.config["dt"]
        damping = self.config["damping"]
        max_force = self.config["max_force"]
        
        for r in results:
            for res in r['batch_results']:
                idx = res['id']
                force = np.array(res['force_vec'])
                
                # Clip forces
                force_mag = np.linalg.norm(force)
                if force_mag > max_force:
                    force = (force / force_mag) * max_force
                
                # Update velocity and position
                self.velocities[idx] = (self.velocities[idx] + force * dt) * damping
                self.positions[idx] += self.velocities[idx] * dt
        
        # Grounding: Center the molecule at origin
        self.positions -= np.mean(self.positions, axis=0)
        
        # Save Snapshot
        self.save_snapshot()
        return len(results)

    def save_snapshot(self):
        # Pass positions and secondary structure labels
        data = {
            "residues": self.positions.tolist(),
            "ss": self.ss_list, # Secondary structure labels (H, S, C)
            "iter": time.time()
        }
        with open("apps/bioswarm_monitor/bio_snapshot.json", "w") as f:
            json.dump(data, f)

    def shutdown(self):
        self.swarm.shutdown()

if __name__ == "__main__":
    # Real PDB Demo
    pdb_file = "simulations/bioswarm/1ubq.pdb"
    engine = BioSwarmEngine(pdb_path=pdb_file if os.path.exists(pdb_file) else None)
    try:
        for i in range(1000000): # Indefinite for visualization
            engine.step(i)
            if (i+1) % 100 == 0:
                print(f"🧬 [BioSwarm] Iteration {i+1} completed.")
            time.sleep(0.01) 
    except KeyboardInterrupt:
        print("\n🛑 [BioSwarm] Stopped by user.")
    engine.shutdown()
