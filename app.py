import streamlit as st
from core.query import JAKEQuery
from core.ingest import JAKEIngest
from core.intelligence import JAKEIntelligence
import os

st.set_page_config(page_title="J.A.K.E - Knowledge Engine", layout="wide")
st.title("🧠 J.A.K.E - Janus AI Knowledge Engine")
st.markdown("Local-first Knowledge Graph with Hybrid Search")

# Sidebar
st.sidebar.header("Controls")
if st.sidebar.button("Run Ingestion"):
    with st.spinner("Ingesting files from raw/..."):
        ingester = JAKEIngest()
        ingester.process_all()
    st.sidebar.success("Ingestion complete!")

if st.sidebar.button("Run Health Check"):
    health = JAKEIntelligence()
    health.run_health_check()

# Main area
query = st.text_input("Ask a question about your knowledge base:", 
                         "What are the key risks in AI infrastructure?")

if st.button("Search (Hybrid)"):
    if query:
        with st.spinner("Searching..."):
            querier = JAKEQuery()
            result = querier.ask(query, use_vector=True)
        st.subheader("Answer")
        st.write(result)
    else:
        st.warning("Please enter a question.")

st.markdown("---")
st.caption("Fully local • Powered by Ollama • Vector + Graph hybrid search")