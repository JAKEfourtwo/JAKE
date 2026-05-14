import sys
import argparse
from pathlib import Path
from core.ingest import JAKEIngest
from core.query import JAKEQuery
from core.intelligence import JAKEIntelligence

def main():
    parser = argparse.ArgumentParser(description="J.A.K.E — Janus AI Knowledge Engine")
    parser.add_argument("command", choices=["ingest", "query", "health"])
    parser.add_argument("query_text", nargs="?", help="Query text for 'query' command")
    
    args = parser.parse_args()
    
    if args.command == "ingest":
        ingester = JAKEIngest()
        ingester.process_all()
    elif args.command == "query":
        if not args.query_text:
            print("Please provide a query: python run.py query \"your question\"")
            return
        querier = JAKEQuery()
        result = querier.ask(args.query_text)
        print(result)
    elif args.command == "health":
        health = JAKEIntelligence()
        health.run_health_check()

if __name__ == "__main__":
    main()