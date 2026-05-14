"""Basic Agentic Workflow for J.A.K.E

Supports multi-step reasoning using the knowledge graph + LLM.
"""

from core.query import JAKEQuery
import ollama

class JAKEAgent:
    def __init__(self):
        self.query_engine = JAKEQuery()
    
    def think(self, goal: str, max_steps: int = 5):
        """Simple ReAct-style agent loop."""
        history = []
        context = ""
        
        for step in range(max_steps):
            prompt = f"""You are a strategic reasoning agent.
Goal: {goal}

Current context from knowledge base:
{context}

History: {history}

What should I do next? (Think step by step or give final answer)"""
            
            response = ollama.chat(
                model="qwen2.5",
                messages=[{"role": "user", "content": prompt}]
            )['message']['content']
            
            history.append(response)
            
            if "final answer" in response.lower() or step == max_steps - 1:
                return response
            
            # Retrieve more context
            new_context = self.query_engine.ask(goal)
            context += "\n" + new_context[:500]
        
        return "\n".join(history)