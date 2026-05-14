import numpy as np
import ollama
import json
from pathlib import Path
import tomli
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleVectorStore:
    def __init__(self, path: str = "graph/embeddings.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.vectors = {}
        self.load()
    
    def load(self):
        if self.path.exists():
            try:
                with open(self.path) as f:
                    data = json.load(f)
                    self.vectors = {k: np.array(v) for k, v in data.items()}
            except:
                self.vectors = {}
    
    def save(self):
        data = {k: v.tolist() for k, v in self.vectors.items()}
        with open(self.path, "w") as f:
            json.dump(data, f)
    
    def add(self, doc_id: str, text: str, model: str = "nomic-embed-text"):
        try:
            resp = ollama.embeddings(model=model, prompt=text[:2000])
            embedding = np.array(resp["embedding"])
            self.vectors[doc_id] = embedding
            self.save()
            return True
        except Exception as e:
            logger.warning(f"Embedding failed for {doc_id}: {e}")
            return False
    
    def search(self, query: str, top_k: int = 5, model: str = "nomic-embed-text"):
        if not self.vectors:
            return []
        try:
            resp = ollama.embeddings(model=model, prompt=query)
            q_vec = np.array(resp["embedding"])
            
            results = []
            for doc_id, vec in self.vectors.items():
                sim = np.dot(q_vec, vec) / (np.linalg.norm(q_vec) * np.linalg.norm(vec))
                results.append((doc_id, float(sim)))
            
            results.sort(key=lambda x: x[1], reverse=True)
            return results[:top_k]
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return []