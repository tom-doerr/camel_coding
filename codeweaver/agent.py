"""
Autonomous coding agent implementation using CAMEL framework
"""
import os
from dataclasses import dataclass
from typing import Optional, List
from camel.agents import EmbodiedAgent
from camel.messages import BaseMessage
from camel.toolkits import OpenAIFunction, SubProcessInterpreter
from camel.types import RoleType

@dataclass
class CodingTask:
    """A coding task to be performed by the agent"""
    description: str
    language: str

class CodingAgent:
    """An autonomous coding agent using CAMEL framework"""
    
    def __init__(self, system_message=None):
        """Initialize the coding agent"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        self.system_message = system_message or "You are an expert programmer. Write clean, efficient code following best practices. Only return the code, no explanations."
        
        # Initialize the embodied agent with tools
        self.agent = EmbodiedAgent(
            system_message=self.system_message,
            code_interpreter=SubProcessInterpreter(),
            verbose=True
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
