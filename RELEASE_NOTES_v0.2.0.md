# v0.2.0 — Agentic + API + Automation

**Release Date:** May 14, 2026

J.A.K.E has evolved from a solid MVP into a much more capable local-first intelligence platform.

## ✨ Highlights

- Full authenticated **FastAPI backend** with JWT
- **Advanced agent** with planning, memory, and reflection
- **Production vector search** foundation (sqlite-vec ready)
- **Automated daily intelligence reports** via GitHub Actions
- New **evaluation & benchmarking** suite
- **Gradio UI** + improved Streamlit experience
- **Multimodal readiness** (vision support)
- Expanded file support and **Obsidian export**

## New Features

### Authenticated API
- New `api/main.py` with JWT authentication
- Protected `/query` and `/report` endpoints
- Easy to extend with real user management

### Advanced Agentic System
- Planning, tool use, short-term + long-term memory
- Reflection capabilities
- Located in `core/advanced_agent.py`

### Vector Search
- New `core/production_vec_store.py` with sqlite-vec foundation
- Better performance path for large-scale vector search

### Automation
- Daily intelligence report generation via GitHub Actions
- Scheduled to run automatically every day

### Developer Experience
- New benchmarking suite (`eval/benchmark.py`)
- Better error handling and logging throughout
- Gradio UI alternative

## Improvements

- Hybrid search now deeply integrated into ingestion and querying
- Expanded file type support (PDF, DOCX, HTML, Markdown, TXT)
- Vision/multimodal support foundation added
- Export to Obsidian / Roam / Logseq
- Significantly improved documentation

## Infrastructure
- Multiple GitHub Actions workflows added:
  - CI
  - Automated releases
  - Daily report scheduling

## Getting Started

```bash
git clone https://github.com/JAKEfourtwo/JAKE.git
cd JAKE
pip install -r requirements.txt

# Try the UIs
streamlit run app.py
# or
python app_gradio.py

# Or run the API
uvicorn api.main:app --reload
```

## What's Next?

We're planning deeper work on:
- Full Tauri desktop application
- Production deployment hardening
- More powerful agent tools

---

**Full Changelog**: [CHANGELOG.md](https://github.com/JAKEfourtwo/JAKE/blob/main/CHANGELOG.md)

**J.A.K.E** — Local-first AI Knowledge Graph OS that turns raw information into structured, compounding intelligence.