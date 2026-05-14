import ollama
import sqlite3
import tomli
from pathlib import Path

class JAKEQuery:
    def __init__(self):
        with open("config.toml", "rb") as f:
            self.config = tomli.load(f)
        self.conn = sqlite3.connect(self.config["paths"]["root"] + "/" + self.config["paths"]["graph_db"])
    
    def ask(self, question: str):
        # Simple retrieval + LLM synthesis
        cursor = self.conn.execute("SELECT subject, predicate, object FROM triples LIMIT 50")
        triples = cursor.fetchall()
        
        context = "\n".join([f"{s} {p} {o}" for s, p, o in triples])
        
        prompt = f"""Use only the provided knowledge to answer the question.
Knowledge:
{context}

Question: {question}

Answer concisely and cite relationships:"""
        
        resp = ollama.chat(
            model=self.config["llm"]["model"],
            messages=[{"role": "user", "content": prompt}]
        )
        return resp['message']['content']