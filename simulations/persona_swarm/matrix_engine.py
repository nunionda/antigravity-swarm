"""
Viral Crisis Matrix: Matrix Engine
Handles parallel sentiment propagation and tipping point detection.
"""
import time
from typing import List
from core.manager import SwarmManager
from simulations.persona_swarm.persona_factory import PersonaFactory, PersonaProfile
from utils.hpc_utils import HPCUtils

class MatrixEngine:
    def __init__(self, swarm_size: int = 32):
        self.factory = PersonaFactory(size=10000)
        self.population = self.factory.generate_population()
        self.swarm = SwarmManager(swarm_size=swarm_size)
        self.history = []

    @HPCUtils.benchmark_latency
    def run_time_step(self, step_id: int, external_pressure: float = 0.0):
        """
        Executes one iteration of sentiment propagation across the swarm.
        """
        # Phase 1: Direct External Impact (Parallel)
        tasks = []
        batch_size = 500
        for i in range(0, len(self.population), batch_size):
            tasks.append({
                "id": f"step_{step_id}_batch_{i}",
                "range": (i, min(i + batch_size, len(self.population))),
                "pressure": external_pressure,
                "complexity": 1
            })
            
        self.swarm.dispatch_batch(tasks)
        
        # Phase 2: Peer-to-Peer Propagation (Shared Memory Context)
        # In a real HPC environment, this would be a vectorized kernel operation.
        new_sentiments = []
        total_sentiment = 0.0
        
        for p in self.population:
            # Simple propagation logic: Sentiment is affected by neighbors
            neighbor_sentiment = sum(self.population[n].sentiment for n in p.neighbors) / len(p.neighbors)
            p.sentiment = (p.sentiment * 0.7) + (neighbor_sentiment * 0.3) - external_pressure
            
            # Bound sentiment
            p.sentiment = max(0.0, min(100.0, p.sentiment))
            total_sentiment += p.sentiment
            
        avg_sentiment = total_sentiment / len(self.population)
        self.history.append(avg_sentiment)
        return avg_sentiment

    def simulate_crisis(self, steps: int = 5, initial_shock: float = 20.0):
        print(f"🎬 [ENGINE] Starting Crisis Simulation for {steps} steps...")
        for i in range(steps):
            # External shock decays over time, but P2P propagation continues
            pressure = initial_shock if i == 0 else max(0, initial_shock - (i * 2))
            current_sentiment = self.run_time_step(i, external_pressure=pressure)
            
            status = "CRITICAL" if current_sentiment < 50 else "STABLE"
            print(f"⏱️ [STEP {i+1}] Avg Sentiment: {current_sentiment:.2f}% | Status: {status}")
            
            if current_sentiment < 30:
                print("🚨 [ALERT] TIPPING POINT REACHED: IRREVERSIBLE BRAND DAMAGE.")
                break
                
        return self.history

    def shutdown(self):
        self.swarm.shutdown()

if __name__ == "__main__":
    engine = MatrixEngine()
    engine.simulate_crisis(steps=5, initial_shock=30.0)
    engine.shutdown()
