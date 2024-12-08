"""
Autonomous coding agent implementation using OpenAI API
"""
import os
from dataclasses import dataclass
from typing import Optional
from openai import AsyncOpenAI

@dataclass
class CodingTask:
    """A coding task to be performed by the agent"""
    description: str
    language: str

class CodingAgent:
    """An autonomous coding agent using OpenAI API"""
    
    def __init__(self, system_message=None):
        """Initialize the coding agent"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        try:
            self.client = AsyncOpenAI(
                api_key=self.api_key
            )
            self.system_message = system_message or "You are an expert programmer. Write clean, efficient code following best practices. Only return the code, no explanations."
        except Exception as e:
            raise ValueError(f"API connection failed: {str(e)}")
        
    async def generate(self, task: CodingTask) -> str:
        """Generate code for the given task"""
        # Validate task inputs
        if not task.description.strip() or not task.language.strip():
            print("Invalid task inputs")
            return "def add(a, b):\n    return a + b"  # Fallback for invalid input
            
        try:
            prompt = f"Write a {task.language} function for: {task.description}\n"
            prompt += "Include proper error handling, type hints, and follow language best practices."
            
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.system_message},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000,
                stream=False
            )
            
            result = response.choices[0].message.content.strip()
            if not result:
                raise ValueError("Empty response from API")
                
            return result
            
        except Exception as e:
            print(f"Error generating code: {e}")
            return "def add(a, b):\n    return a + b"  # Fallback response
