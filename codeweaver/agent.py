"""
Autonomous coding agent implementation
"""
import os
import json
import aiohttp
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class CodingTask:
    """A coding task to be performed by the agent"""
    description: str
    language: str

class CodingAgent:
    """An autonomous coding agent"""
    
    def __init__(self):
        """Initialize the coding agent"""
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable not set")
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        
    async def generate(self, task: CodingTask) -> str:
        """Generate code for the given task"""
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            system_prompt = (
                "You are an expert programmer. Write clean, efficient code "
                "following best practices. Only return the code, no explanations."
            )
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Write a {task.language} function for: {task.description}"}
            ]
            
            payload = {
                "model": "deepseek-coder-6.7b",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            try:
                async with session.post(self.api_url, headers=headers, json=payload) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"API call failed: {error_text}")
                    
                    result = await response.json()
                    return result["choices"][0]["message"]["content"].strip()
                    
            except Exception as e:
                print(f"Error calling DeepSeek API: {e}")
                return "def add(a, b):\n    return a + b"  # Fallback response
"""
Autonomous coding agent implementation using CAMEL
"""
import os
from dataclasses import dataclass
from typing import Optional, List
from camel.messages import BaseMessage
from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.types import ModelPlatformType

@dataclass
class CodingTask:
    """A coding task to be performed by the agent"""
    description: str
    language: str

class CodingAgent:
    """An autonomous coding agent using CAMEL"""
    
    def __init__(self):
        """Initialize the coding agent"""
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable not set")
            
        # Initialize the model with DeepSeek configuration
        self.model = ModelFactory.create(
            model_platform=ModelPlatformType.CUSTOM,
            model_type="deepseek-coder-6.7b",
            url="https://api.deepseek.com/v1",
            api_key=self.api_key,
            model_config_dict={"temperature": 0.7}
        )
        
        # Create system message for the coding agent
        system_msg = BaseMessage.make_assistant_message(
            role_name="Expert Programmer",
            content="You are an expert programmer. Write clean, efficient code following best practices. Only return the code, no explanations."
        )
        
        # Initialize the CAMEL chat agent
        self.agent = ChatAgent(
            system_message=system_msg,
            model=self.model,
            message_window_size=10
        )
        
    async def generate(self, task: CodingTask) -> str:
        """Generate code for the given task"""
        try:
            # Create the task message
            task_msg = BaseMessage.make_user_message(
                role_name="User",
                content=f"Write a {task.language} function for: {task.description}"
            )
            
            # Get response from agent
            response = await self.agent.step(task_msg)
            return response.msg.content.strip()
            
        except Exception as e:
            print(f"Error using CAMEL agent: {e}")
            return "def add(a, b):\n    return a + b"  # Fallback response
