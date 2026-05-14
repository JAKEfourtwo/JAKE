"""Hybrid Search Demo for J.A.K.E

Demonstrates combined symbolic (graph) + semantic (vector) search.
"""

from core.query import JAKEQuery
from core.ingest import JAKEIngest
import argparse


def main():
    parser = argparse.ArgumentParser(description="J.A.K.E Hybrid Search Demo")
    parser.add_argument("--ingest", action="store_true", help="Ingest sample data first")
    parser.add_argument("query", nargs="?", default="What are the main risks in AI infrastructure?", help="Your question")
    args = parser.parse_args()

    if args.ingest:
        print("Ingesting sample data...")
        ingester = JAKEIngest()
        ingester.process_all()
        print("Ingestion complete.\n")

    print(f"Query: {args.query}\n")
    querier = JAKEQuery()
    
    # Hybrid search (graph + vector)
    result = querier.ask(args.query, use_vector=True)
    print("=== Hybrid Search Result ===")
    print(result)

    print("\n=== Done ===")


if __name__ == "__main__":
    main()