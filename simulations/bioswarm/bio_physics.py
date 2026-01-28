"""
BioSwarm: Molecular Dynamics Kernel
Simulates physical forces acting on amino acid residues in a protein chain.
"""
import numpy as np
import random
from core.worker import AgentWorker

class BioPhysicsKernel(AgentWorker):
    def execute(self, task: dict) -> dict:
        """
        Calculates forces for a batch of residues.
        Includes simplified Lennard-Jones (van der Waals) and bond constraints.
        """
        agent_range = task.get("range")
        positions = np.array(task.get("positions"), dtype=np.float32) # Current positions of all residues
        residue_count = len(positions)
        
        results = []
        for i in range(agent_range[0], agent_range[1]):
            # 1. Internal Chain Constraints (Backbone Bond)
            # Each residue 'i' is bonded to 'i-1' and 'i+1'
            f_bond = np.zeros(3, dtype=np.float32)
            k_spring = 0.5 # Bond stiffness
            r0 = 3.8 # Ideal C-alpha distance (Angstroms)
            
            for neighbor_idx in [i-1, i+1]:
                if 0 <= neighbor_idx < residue_count:
                    diff = positions[neighbor_idx] - positions[i]
                    dist = np.linalg.norm(diff)
                    if dist > 0:
                        f_bond += k_spring * (dist - r0) * (diff / dist)
            
            # 2. Non-bonded Interactions (Lennard-Jones / VdW)
            f_vdw = np.zeros(3, dtype=np.float32)
            sample_count = 12 # Slightly increased sampling
            epsilon = 0.12 # Re-tuned
            sigma = 3.82 
            
            for _ in range(sample_count):
                target_idx = random.randint(0, residue_count - 1)
                if abs(target_idx - i) > 1: # Only non-bonded neighbors
                    diff = positions[target_idx] - positions[i]
                    dist_sq = np.dot(diff, diff)
                    if 0.01 < dist_sq < 144.0: # Interaction cutoff squared
                        dist = np.sqrt(dist_sq)
                        s_d = sigma / dist
                        f_mag = 24 * epsilon * (2 * (s_d**12) - (s_d**6)) / dist
                        # Cap force magnitude per interaction
                        f_mag = np.clip(f_mag, -50.0, 50.0)
                        f_vdw += -f_mag * (diff / dist)
            
            # Total Force
            f_total = f_bond + f_vdw
            
            results.append({
                "id": i,
                "force_vec": f_total.tolist(),
                "alignment": "128_bit"
            })
            
        return {
            "worker_id": self.worker_id,
            "status": "COMPLETED",
            "batch_results": results
        }
