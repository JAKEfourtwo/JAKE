import gradio as gr
from core.query import JAKEQuery
from core.ingest import JAKEIngest
from core.intelligence import JAKEIntelligence

def ingest_data():
    ingester = JAKEIngest()
    ingester.process_all()
    return "Ingestion complete!"

def health_check():
    health = JAKEIntelligence()
    health.run_health_check()
    return "Health check completed (see console)"

def hybrid_search(question):
    querier = JAKEQuery()
    return querier.ask(question, use_vector=True)

with gr.Blocks(title="J.A.K.E - Knowledge Engine") as demo:
    gr.Markdown("# 🧠 J.A.K.E - Janus AI Knowledge Engine")
    gr.Markdown("Local-first Hybrid Knowledge Graph")
    
    with gr.Row():
        ingest_btn = gr.Button("Ingest Data")
        health_btn = gr.Button("Run Health Check")
    
    ingest_btn.click(ingest_data, outputs=gr.Textbox())
    health_btn.click(health_check, outputs=gr.Textbox())
    
    question = gr.Textbox(label="Ask a question", value="What are the key risks in AI infrastructure?")
    search_btn = gr.Button("Hybrid Search")
    output = gr.Textbox(label="Answer", lines=10)
    
    search_btn.click(hybrid_search, inputs=question, outputs=output)

demo.launch()