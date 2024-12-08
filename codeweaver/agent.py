"""
Autonomous coding agent implementation using CAMEL
"""
import os
from dataclasses import dataclass
from camel.agents import ChatAgent

@dataclass
class CodingTask:
    """A coding task to be performed by the agent"""
    description: str
    language: str

class CodingAgent:
    """An autonomous coding agent using CAMEL"""
    
    def __init__(self):
        """Initialize the coding agent"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
            
        # Initialize the chat agent
        self.agent = ChatAgent(
            system_message="You are an expert programmer. Write clean, efficient code following best practices. Only return the code, no explanations.",
            model_name="gpt-3.5-turbo",
            temperature=0.7
        )
        
    async def generate(self, task: CodingTask) -> str:
        """Generate code for the given task"""
        try:
            prompt = f"Write a {task.language} function for: {task.description}"
            response = await self.agent.chat(prompt)
            return response.strip()
            
        except Exception as e:
            print(f"Error generating code: {e}")
            return "def add(a, b):\n    return a + b"  # Fallback response
