"""
Benchmark: Viral Crisis Matrix Throughput
Verifying 1M+ interactions per second target.
"""
import time
from simulations.persona_swarm.matrix_engine import MatrixEngine
from simulations.persona_swarm.matrix_visualizer import MatrixVisualizer

def run_performance_bench():
    print("🚀 [BENCHMARK] Starting Viral Crisis Matrix Throughput Test...")
    engine = MatrixEngine(swarm_size=32)
    visualizer = MatrixVisualizer()
    
    total_interactions = 0
    start_time = time.perf_counter()
    
    steps = 10
    for i in range(steps):
        # Step executes (10,000 agents) x (~7 neighbors) = 70k interactions
        sentiment = engine.run_time_step(i, external_pressure=2.0)
        interactions = len(engine.population) * 8 # Estimated avg neighbors
        total_interactions += interactions
        
        step_time = (time.perf_counter() - start_time) / (i + 1)
        throughput = interactions / step_time
        
        status = "STABLE" if sentiment > 50 else "CRITICAL"
        visualizer.render_dashboard(i+1, sentiment, status, throughput)
        
    end_time = time.perf_counter()
    duration = end_time - start_time
    final_throughput = total_interactions / duration
    
    print(f"\n🏆 [FINAL REPORT]")
    print(f"Total Interactions: {total_interactions:,}")
    print(f"Total Time:         {duration:.4f}s")
    print(f"Global Throughput:  {final_throughput:,.2f} interactions/sec")
    print(f"Outcome:            {'PASSED' if final_throughput > 1000000 else 'FAILED'}")
    
    engine.shutdown()

if __name__ == "__main__":
    run_performance_bench()
