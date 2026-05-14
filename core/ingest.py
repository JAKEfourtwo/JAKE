import json
import hashlib
from pathlib import Path
import ollama
import sqlite3
from pypdf import PdfReader
import tomli

class JAKEIngest:
    def __init__(self):
        with open("config.toml", "rb") as f:
            self.config = tomli.load(f)
        
        self.root = Path(self.config["paths"]["root"])
        self.db_path = self.root / self.config["paths"]["graph_db"]
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.conn = sqlite3.connect(self.db_path)
        self._init_db()
    
    def _init_db(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS triples (
                id TEXT PRIMARY KEY,
                subject TEXT, predicate TEXT, object TEXT,
                confidence REAL, timestamp TEXT, source TEXT
            );
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                filename TEXT,
                content TEXT,
                timestamp TEXT
            );
        """)
        self.conn.commit()
    
    def extract_text(self, filepath: Path) -> str:
        if filepath.suffix.lower() == ".pdf":
            reader = PdfReader(filepath)
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        return filepath.read_text(encoding="utf-8", errors="ignore")
    
    def llm_extract(self, text: str):
        prompt = f"""Extract structured knowledge from the text. Return ONLY valid JSON:
{{
  "entities": ["Entity1", "Entity2"],
  "relations": [
    {{"subject": "", "predicate": "", "object": ""}}
  ],
  "facts": ["key fact 1", "key fact 2"]
}}
Text: {text[:self.config["ingest"]["max_chunk_size"]]}"""
        
        response = ollama.chat(
            model=self.config["llm"]["model"],
            messages=[{"role": "user", "content": prompt}]
        )
        try:
            return json.loads(response['message']['content'])
        except:
            return {"entities": [], "relations": [], "facts": []}
    
    def process_file(self, filepath: Path):
        print(f"Processing {filepath.name}...")
        text = self.extract_text(filepath)
        
        data = self.llm_extract(text)
        
        # Store document
        doc_id = hashlib.md5(text.encode()).hexdigest()[:16]
        self.conn.execute(
            "INSERT OR REPLACE INTO documents VALUES (?, ?, ?, datetime('now'))",
            (doc_id, filepath.name, text[:2000])
        )
        
        # Store triples
        for rel in data.get("relations", []):
            tid = hashlib.md5(f"{rel.get('subject')}{rel.get('predicate')}{rel.get('object')}".encode()).hexdigest()
            self.conn.execute(
                "INSERT OR REPLACE INTO triples VALUES (?, ?, ?, ?, ?, datetime('now'), ?)",
                (tid, rel.get('subject'), rel.get('predicate'), rel.get('object'), 0.8, filepath.name)
            )
        
        # Create basic wiki page
        wiki_dir = self.root / "wiki/entities"
        wiki_dir.mkdir(parents=True, exist_ok=True)
        for entity in data.get("entities", [])[:10]:
            page = wiki_dir / f"{entity.replace(' ', '_')}.md"
            if not page.exists():
                page.write_text(f"# {entity}\n\n## Facts\n\n## Relations\n\n[[source:{filepath.name}]]")
        
        self.conn.commit()
        print(f"✅ {filepath.name} → {len(data.get('relations', []))} relations")
    
    def process_all(self):
        raw_dir = self.root / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        for file in raw_dir.glob("**/*.*"):
            if file.is_file():
                self.process_file(file)