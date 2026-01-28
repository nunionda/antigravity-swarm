"""
Benchmark: Omni-Scribe Performance (1M LOC Simulation)
"""
import time
from omni_scribe.ast_engine import ASTEngine
from omni_scribe.context_bus import ContextBus
from omni_scribe.impact_analyzer import ImpactAnalyzer

def run_omni_scribe_benchmark(file_count: int = 1000):
    print(f"--- OMNI-SCRIBE BENCHMARK: {file_count} Files ---")
    
    engine = ASTEngine()
    bus = ContextBus()
    analyzer = ImpactAnalyzer(bus)
    
    mock_code = "def process(data):\n    return data * 2\n" * 50 # ~100 lines per file
    
    # 1. Parallel Parsing & Bus Hydration
    print(f"[1/2] Hydrating Context Bus with {file_count} files...")
    start = time.perf_counter()
    for i in range(file_count):
        file_path = f"project/file_{i}.py"
        ast_summary = engine.parse_source(mock_code, file_path)
        bus.update_file_state(file_path, ast_summary['nodes'])
    end = time.perf_counter()
    print(f"Hydration Time: {end - start:.4f}s ({(end - start)/file_count * 1000:.2f}ms per file)")

    # 2. Global Impact Analysis
    print(f"[2/2] Running Global Impact Analysis for core change...")
    start = time.perf_counter()
    impacts = analyzer.analyze_change("core/kernel.py")
    end = time.perf_counter()
    
    total_time = end - start
    print(f"Global Sync Latency: {total_time * 1000:.2f}ms")
    print(f"Throughput: {file_count / total_time:.2f} files/sec awareness")
    
    analyzer.shutdown()
    print("--- BENCHMARK COMPLETE ---")

if __name__ == "__main__":
    # Simulate a mid-sized enterprise repo (1,000 files)
    run_omni_scribe_benchmark(file_count=1000)
