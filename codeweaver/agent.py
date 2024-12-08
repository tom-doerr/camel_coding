"""
Autonomous coding agent implementation using DeepSeek
"""
import os
from dataclasses import dataclass
from typing import Optional
import deepseek

@dataclass
class CodingTask:
    """A coding task to be performed by the agent"""
    description: str
    language: str
    test_requirements: Optional[str] = None

class CodingAgent:
    """An autonomous coding agent using DeepSeek"""
    
    def __init__(self):
        """Initialize the coding agent"""
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable not set")
            
        # Initialize the client
        deepseek.api_key = self.api_key
        
    async def generate(self, task: CodingTask) -> str:
        """Generate code for the given task"""
        try:
            prompt = f"""Write a {task.language} function for: {task.description}
            
            Requirements:
            - Include docstrings and type hints
            - Follow PEP 8 style guidelines
            - Include error handling where appropriate
            """
            
            if task.test_requirements:
                prompt += f"\nTest requirements:\n{task.test_requirements}"

            response = await deepseek.Completion.create(
                model="deepseek-coder",
                prompt=prompt,
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].text.strip()
            
        except Exception as e:
            print(f"Error generating code: {e}")
            return None
