"""Evaluation & Benchmarking Suite for J.A.K.E

Measures latency, accuracy, and scalability of hybrid search.
"""

import time
import statistics
from core.query import JAKEQuery

class JAKEBenchmark:
    def __init__(self):
        self.querier = JAKEQuery()
    
    def run_latency_benchmark(self, queries: list, use_vector=True):
        latencies = []
        for q in queries:
            start = time.time()
            _ = self.querier.ask(q, use_vector=use_vector)
            latencies.append(time.time() - start)
        
        return {
            "avg_latency": statistics.mean(latencies),
            "min_latency": min(latencies),
            "max_latency": max(latencies),
            "queries_tested": len(queries)
        }
    
    def compare_graph_vs_hybrid(self, queries: list):
        graph_only = self.run_latency_benchmark(queries, use_vector=False)
        hybrid = self.run_latency_benchmark(queries, use_vector=True)
        return {"graph_only": graph_only, "hybrid": hybrid}

if __name__ == "__main__":
    benchmark = JAKEBenchmark()
    test_queries = [
        "Key risks in AI infrastructure supply chain",
        "Impact of geopolitics on semiconductor industry",
        "Future trends in sovereign AI"
    ]
    print(benchmark.compare_graph_vs_hybrid(test_queries))