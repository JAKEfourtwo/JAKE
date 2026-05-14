# J.A.K.E Demo Notebook

This notebook demonstrates the full J.A.K.E pipeline.

## 1. Setup

```python
!pip install -r requirements.txt
```

## 2. Ingest Sample Data

```python
from core.ingest import JAKEIngest

ingester = JAKEIngest()
ingester.process_all()   # Processes everything in raw/
```

## 3. Run Hybrid Query

```python
from core.query import JAKEQuery

q = JAKEQuery()
result = q.ask("What are the key relationships in AI infrastructure?", use_vector=True)
print(result)
```

## 4. Health Check

```python
from core.intelligence import JAKEIntelligence

health = JAKEIntelligence()
health.run_health_check()
```

## 5. Vector Search Directly

```python
from core.vector_store import SimpleVectorStore

vs = SimpleVectorStore()
results = vs.search("AI infrastructure risks", top_k=3)
print(results)
```

---

**Tip**: Drop your own PDFs/Markdown into `raw/` and re-run ingestion.