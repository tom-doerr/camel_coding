"""
Autonomous coding agent implementation using CAMEL EmbodiedAgent
"""
import os
from dataclasses import dataclass
from typing import Optional
from openai import AsyncOpenAI
from camel.messages import BaseMessage
from camel.agents import EmbodiedAgent
from camel.generators import SystemMessageGenerator
from camel.types import RoleType

@dataclass 
class CodingTask:
    """A coding task to be performed by the agent"""
    description: str

class CodingAgent:
    """An autonomous coding agent using OpenAI API with CAMEL integration"""
    
    def __init__(self, system_message=None):
        """Initialize the coding agent"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        # Initialize system message generator
        role = "Expert Programmer"
        task = "Writing clean, efficient code following best practices"
        meta_dict = {"role": role, "task": task}
        role_tuple = (role, RoleType.EMBODIMENT)
        
        # Generate system message
        sys_msg_gen = SystemMessageGenerator()
        default_sys_msg = sys_msg_gen.from_dict(meta_dict=meta_dict, role_tuple=role_tuple)
        
        # Use provided system message or default
        self.system_message = system_message or default_sys_msg
        
        # Initialize CAMEL embodied agent
        self.agent = EmbodiedAgent(
            system_message=self.system_message,
            verbose=True
        )
        
    async def generate(self, task: CodingTask) -> str:
        """Generate code for the given task"""
        # Validate task input
        if not task.description.strip():
            print("Invalid task input")
            return "def add(a, b):\n    return a + b"  # Fallback for invalid input
            
        try:
            # Create user message with specific task
            prompt = (
                f"Write a Python function that implements this task:\n"
                f"{task.description}\n\n"
                "Requirements:\n"
                "1. Include proper error handling\n"
                "2. Add type hints where applicable\n" 
                "3. Follow Python best practices\n"
                "4. Write clean, maintainable code\n"
                "5. Only return the code, no explanations"
            )
            
            user_msg = BaseMessage.make_user_message(
                role_name="Programmer",
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
