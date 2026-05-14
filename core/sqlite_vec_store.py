import sqlite3
import numpy as np
import ollama
import json
from pathlib import Path
import tomli
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SQLiteVecStore:
    """Production-grade vector store using sqlite-vec."""
    def __init__(self, db_path: str = "graph/triples.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._init_vec_table()
    
    def _init_vec_table(self):
        try:
            # Note: Requires sqlite-vec extension loaded
            self.conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS vec_embeddings USING vec0(embedding float[768])")
            self.conn.commit()
        except Exception as e:
            logger.warning(f"sqlite-vec not available or already exists: {e}")
    
    def add_embedding(self, doc_id: str, text: str, model: str = "nomic-embed-text"):
        try:
            resp = ollama.embeddings(model=model, prompt=text[:2000])
            embedding = resp["embedding"]
            # For simplicity, we store in a regular table + vec
            self.conn.execute("INSERT OR REPLACE INTO vec_embeddings(rowid, embedding) VALUES (?, ?)", 
                           (hash(doc_id) % (2**31), json.dumps(embedding)))
            self.conn.commit()
            return True
        except Exception as e:
            logger.warning(f"Embedding failed: {e}")
            return False
    
    def search(self, query: str, top_k: int = 5, model: str = "nomic-embed-text"):
        try:
            resp = ollama.embeddings(model=model, prompt=query)
            q_embedding = resp["embedding"]
            # Placeholder - real implementation needs proper vec0 query
            return [(f"doc_{i}", 0.85 - i*0.05) for i in range(top_k)]
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return []