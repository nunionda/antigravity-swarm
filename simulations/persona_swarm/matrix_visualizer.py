"""
Viral Crisis Matrix: Visualizer
CLI Dashboard for real-time sentiment tracking.
"""
import os
import time

class MatrixVisualizer:
    @staticmethod
    def render_sentiment_bar(sentiment: float, width: int = 40):
        filled_len = int(width * sentiment / 100)
        bar = '█' * filled_len + '-' * (width - filled_len)
        color = "\033[92m" if sentiment > 70 else "\033[93m" if sentiment > 40 else "\033[91m"
        return f"{color}[{bar}] {sentiment:6.2f}%\033[0m"

    @staticmethod
    def clear_screen():
        os.system('clear' if os.name == 'posix' else 'cls')

    @staticmethod
    def render_dashboard(step: int, sentiment: float, status: str, throughput: float):
        # MatrixVisualizer.clear_screen()
        print(f"\n--- VIRAL CRISIS MATRIX DASHBOARD (Step {step}) ---")
        print(f"STATUS:     {status}")
        print(f"SENTIMENT:  {MatrixVisualizer.render_sentiment_bar(sentiment)}")
        print(f"THROUGHPUT: {throughput:,.2f} interactions/sec")
        print("-" * 50)

if __name__ == "__main__":
    visualizer = MatrixVisualizer()
    visualizer.render_dashboard(1, 85.5, "STABLE", 1250000.0)
