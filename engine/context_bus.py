"""
Omni-Scribe Context Bus
High-speed shared memory storage for project-wide AST data.
"""
from core.memory_bus import MemoryBus
from utils.hpc_utils import HPCUtils

class ContextBus(MemoryBus):
    def __init__(self, buffer_size: int = 10000):
        super().__init__(buffer_size=buffer_size)
        # Store for the 'Live Digital Twin' (Project State)
        self.project_state = {}
        # Memory-aligned metadata buffer (Step 01)
        self.registry_buffer = HPCUtils.align_buffer(2048, alignment=16)

    def update_file_state(self, file_path: str, ast_summary: dict):
        """
        Updates the global context with new AST data.
        Bypasses standard serialization overhead where possible.
        """
        self.project_state[file_path] = ast_summary
        # Publish notification to the swarm
        self.publish({
            "type": "CONTEXT_UPDATE",
            "file": file_path,
            "scope": "GLOBAL"
        })

    def get_context(self) -> dict:
        """
        Returns the entire live context of the project.
        """
        return self.project_state

if __name__ == "__main__":
    bus = ContextBus()
    bus.update_file_state("main.py", {"functions": ["init", "run"]})
    print(f"[CONTEXT] Current files in bus: {list(bus.get_context().keys())}")
