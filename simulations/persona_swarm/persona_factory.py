"""
Viral Crisis Matrix: Persona Factory
Generates 10,000+ high-fidelity personas with psychological profiles.
"""
import random
from typing import List, Dict
from utils.hpc_utils import HPCUtils

class PersonaProfile:
    __slots__ = ['id', 'loyalty', 'influence', 'critical_thinking', 'sentiment', 'neighbors']
    
    def __init__(self, agent_id: int):
        self.id = agent_id
        # Psychological Markers (0-100)
        self.loyalty = random.uniform(0, 100)
        self.influence = random.uniform(1.0, 10.0)
        self.critical_thinking = random.uniform(0, 100)
        # Current State
        self.sentiment = 100.0 # Starting healthy
        self.neighbors = [] # P2P Influence Network

class PersonaFactory:
    def __init__(self, size: int = 10000):
        self.size = size
        # Memory-aligned state buffer for fast vectorized access
        self.sentiment_buffer = HPCUtils.align_buffer(size, alignment=16)
        
    def generate_population(self) -> List[PersonaProfile]:
        print(f"🏭 [FACTORY] Generating {self.size} personas with psychological depth...")
        population = [PersonaProfile(i) for i in range(self.size)]
        
        # Build an influence mesh (Small-world network simulation)
        print(f"🕸️ [FACTORY] Building influence mesh (P2P network)...")
        for p in population:
            # Each person listens to 5-10 random peers
            p.neighbors = [random.randint(0, self.size - 1) for _ in range(random.randint(5, 10))]
            
        return population

if __name__ == "__main__":
    factory = PersonaFactory(size=1000)
    pop = factory.generate_population()
    print(f"✅ [FACTORY] Sample Persona {pop[0].id}: Loyalty={pop[0].loyalty:.2f}, Neighbors={len(pop[0].neighbors)}")
