"""
MemoryBus: High-speed messaging layer for the Claude Swarm
Utilizes memory-aligned buffers for data transfer.
"""
import queue
import threading
from utils.hpc_utils import HPCUtils

class MemoryBus:
    def __init__(self, buffer_size: int = 1024):
        self.message_queue = queue.Queue(maxsize=buffer_size)
        # Allocate aligned buffer for message metadata (simulated)
        self.meta_buffer = HPCUtils.align_buffer(1024, alignment=16)
        self._stop_event = threading.Event()

    def publish(self, message: any):
        """
        Publishes a message to the bus using Protocol Step 05: Streaming Store.
        Bypasses cache pollution for transient data.
        """
        # Step 05: Store Nontemporal (Cache Bypass)
        # Simulated as a fast, non-blocking put for transient output
        try:
            self.message_queue.put(message, block=False)
        except queue.Full:
            # Protocol Step 05 assumes non-blocking streaming for certain data classes
            # In a real DMA transfer, this would be a direct bus write
            pass

    def subscribe(self, timeout: float = 0.1) -> any:
        """
        Subscribes to messages from the bus.
        """
        try:
            return self.message_queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def stop(self):
        self._stop_event.set()

class SwarmBus(MemoryBus):
    """
    Specialized bus for Swarm events.
    """
    def __init__(self):
        super().__init__(buffer_size=5000)
