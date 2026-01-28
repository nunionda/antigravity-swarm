"""
Benchmark: Antigravity Transformer vs Scale (100k LOC)
"""
import time
from omni_scribe.transformer_core import TransformerCore
from omni_scribe.monolith_mock import generate_legacy_monolith

def run_scale_benchmark(file_count: int = 500):
    # Assuming avg 200 lines per mock file = 100k LOC
    print(f"--- TRANSFORMER SCALE BENCHMARK: {file_count} Files (~100k LOC) ---")
    
    # 1. Generate Scale Monolith
    generate_legacy_monolith("omni_scribe/scale_repo", file_count)
    files = [f"legacy_file_{i}.js" for i in range(file_count)]
    
    # 2. Run Transformation
    transformer = TransformerCore(swarm_size=32)
    
    start = time.perf_counter()
    results = transformer.transform_project(files)
    end = time.perf_counter()
    
    total_time = end - start
    throughput = file_count / total_time
    
    print(f"\n📊 [REPORT]")
    print(f"Total Files: {file_count}")
    print(f"Total Time:  {total_time:.4f}s")
    print(f"Throughput:  {throughput:.2f} files/sec")
    print(f"Outcome:     {'SUCCESS' if total_time < 5.0 else 'FAILED'}")
    
    transformer.shutdown()
    print("--- BENCHMARK COMPLETE ---")

if __name__ == "__main__":
    run_scale_benchmark(file_count=500)
