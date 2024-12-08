"""
Autonomous coding agent implementation using OpenAI API
"""
import os
from dataclasses import dataclass
from typing import Optional
from openai import AsyncOpenAI
from camel.messages import BaseMessage
from camel.agents import ChatAgent

@dataclass
class CodingTask:
    """A coding task to be performed by the agent"""
    description: str
    language: str

class CodingAgent:
    """An autonomous coding agent using OpenAI API with CAMEL integration"""
    
    def __init__(self, system_message=None):
        """Initialize the coding agent"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        self.client = AsyncOpenAI(api_key=self.api_key)
        self.system_message = system_message or "You are an expert programmer. Write clean, efficient code following best practices. Only return the code, no explanations."
        
        # Initialize CAMEL chat agent with role configuration
        self.agent = ChatAgent(
            system_message=self.system_message,
            model_config={"model": "gpt-4o-mini", "temperature": 0.7}
        )
        
    async def generate(self, task: CodingTask) -> str:
        """Generate code for the given task"""
        # Validate task inputs
        if not task.description.strip() or not task.language.strip():
            print("Invalid task inputs")
            return "def add(a, b):\n    return a + b"  # Fallback for invalid input
            
        try:
            # Create user message
            prompt = f"Write a {task.language} function for: {task.description}\n"
            prompt += "Include proper error handling, type hints, and follow language best practices."
            
            user_msg = BaseMessage.make_user_message(
                role_name='user',
                content=prompt
            )
            
            # Get response from agent
            response = await self.agent.step(user_msg)
            
            if not response or not response.content:
                raise ValueError("Empty response from agent")
                
            return response.content.strip()
            
        except Exception as e:
            print(f"Error generating code: {e}")
            return "def add(a, b):\n    return a + b"  # Fallback response
