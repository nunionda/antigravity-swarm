"""
LivingTwin: Agent Dynamics Kernel
Defines behavioral rules for 100,000 agents.
"""
import random
from dataclasses import dataclass
import random
from core.worker import AgentWorker

@dataclass
class AgentState:
    __slots__ = ['id', 'x', 'y', 'wealth', 'happiness']
    id: int
    x: float
    y: float
    wealth: float
    happiness: float

class DynamicsKernel(AgentWorker):
    def execute(self, task: dict) -> dict:
        """
        Processes a batch of agent states based on grid-following rules.
        """
        agent_range = task.get("range")
        pressure = task.get("pressure", 0.0)
        
        results = []
        for i in range(agent_range[0], agent_range[1]):
            # agent_type: 0 for Pedestrian, 1 for Vehicle
            # For simplicity, we assume the task gives us hints or indices define type
            # Simulation: 20% vehicles, 80% pedestrians
            is_vehicle = (i % 5 == 0)
            
            if is_vehicle:
                # Vehicles move fast along grid lines
                # x-axis or y-axis movement based on ID
                if (i // 5) % 2 == 0:
                    dx, dy = random.uniform(5.0, 10.0), 0
                else:
                    dx, dy = 0, random.uniform(5.0, 10.0)
            else:
                # Pedestrians move more visibly
                dx = random.uniform(-2.0, 2.0)
                dy = random.uniform(-2.0, 2.0)
            
            speed = (dx**2 + dy**2)**0.5
            wealth_delta = random.uniform(-0.1, 0.1) # Restored
            
            results.append({
                "id": i,
                "pos_delta": (dx, dy),
                "speed": speed,
                "wealth_delta": wealth_delta, # Restored
                "type": 1 if is_vehicle else 0,
                "alignment": "128_bit"
            })
            
        return {
            "worker_id": self.worker_id,
            "status": "COMPLETED",
            "batch_results": results
        }
