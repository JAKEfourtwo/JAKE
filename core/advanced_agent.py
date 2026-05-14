"""Advanced Agentic System for J.A.K.E

Features:
- Tool use
- Short-term + long-term memory
- Planning + reflection
"""

from core.query import JAKEQuery
import ollama
import json

class AdvancedJAKEAgent:
    def __init__(self):
        self.query = JAKEQuery()
        self.memory = []          # Short-term
        self.long_term_memory = {}  # Simple persistent memory
    
    def plan(self, goal: str):
        prompt = f"Break this goal into 3-5 clear steps: {goal}"
        response = ollama.chat(model="qwen2.5", messages=[{"role":"user", "content":prompt}]) 
        return response['message']['content']
    
    def execute_step(self, step: str):
        context = self.query.ask(step, use_vector=True)
        self.memory.append({"step": step, "context": context})
        return context
    
    def reflect(self, goal: str):
        prompt = f"Reflect on progress toward: {goal}\nMemory: {json.dumps(self.memory[-3:])}"
        return ollama.chat(model="qwen2.5", messages=[{"role":"user", "content":prompt}])['message']['content']
    
    def run(self, goal: str, max_steps=6):
        plan = self.plan(goal)
        print("Plan:", plan)
        
        for i in range(max_steps):
            step = f"Step {i+1}: {goal}"
            result = self.execute_step(step)
            reflection = self.reflect(goal)
            if "goal achieved" in reflection.lower():
                return reflection
        return "Max steps reached. Final reflection: " + self.reflect(goal)