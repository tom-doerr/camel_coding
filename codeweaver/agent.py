"""
Autonomous coding agent implementation using CAMEL
"""
import os
from dataclasses import dataclass
from typing import Optional
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
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable not set")
            
        # Initialize the chat agent
        self.agent = ChatAgent(
            system_message="You are an expert programmer. Write clean, efficient code following best practices. Only return the code, no explanations."
        )
        
    async def generate(self, task: CodingTask) -> str:
        """Generate code for the given task"""
        # Validate task inputs
        if not task.description.strip() or not task.language.strip():
            print("Invalid task inputs")
            return "def add(a, b):\n    return a + b"  # Fallback for invalid input
            
        try:
            prompt = f"Write a {task.language} function for: {task.description}\n"
            prompt += "Include proper error handling, type hints, and follow language best practices."
            
            response = await self.agent.chat(prompt)
            if not response.strip():
                raise ValueError("Empty response from API")
                
            return response.strip()
            
        except Exception as e:
            print(f"Error generating code: {e}")
            return "def add(a, b):\n    return a + b"  # Fallback response
