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
    
    def __init__(self, system_message=None, model="openai"):
        """Initialize the coding agent
        
        Args:
            system_message: Optional custom system message
            model: Model to use - either 'openai' or 'deepseek'
        """
        self.model = model.lower()
        
        if self.model == "openai":
            self.api_key = os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set")
        elif self.model == "deepseek":
            self.api_key = os.getenv("DEEPSEEK_API_KEY")
            if not self.api_key:
                raise ValueError("DEEPSEEK_API_KEY environment variable not set")
        else:
            raise ValueError(f"Unsupported model: {model}")

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
        
    async def _generate_with_deepseek(self, prompt: str) -> str:
        """Generate code using DeepSeek API"""
        client = AsyncOpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com/v1"
        )
        
        response = await client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content

    async def generate(self, task: CodingTask) -> str:
        """Generate code for the given task"""
        # Validate task input
        if not task.description.strip():
            print("Invalid task input")
            return "def add(a, b):\n    return a + b"  # Fallback for invalid input
            
        try:
            # Create prompt
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
            
            # Get response based on model
            if self.model == "deepseek":
                content = await self._generate_with_deepseek(prompt)
            else:
                user_msg = BaseMessage.make_user_message(
                    role_name="Programmer",
                    content=prompt
                )
                response = await self.agent.step(user_msg)
                content = response.content
            
            if not response or not response.content:
                raise ValueError("Empty response from agent")
            
            # Extract code from response
            content = response.content.strip()
            
            if not content:
                raise ValueError("Empty response from agent")
                
            # Look for code block after "> Code:" marker
            if "> Code:" in content:
                code = content.split("> Code:")[1].strip()
            else:
                # Verify content looks like code
                if not any(keyword in content.lower() for keyword in ['def ', 'class ', 'import ', 'from ']):
                    raise ValueError("Response does not contain valid code")
                code = content
                
            # Remove any trailing logging/debug info
            if "INFO -" in code:
                code = code.split("INFO -")[0].strip()
                
            if not code:
                raise ValueError("No code found in response")
                
            return code
            
        except Exception as e:
            print(f"Error generating code: {e}")
            # Return a more informative error response
            return """def error_response():
    \"\"\"This is a placeholder returned due to an error in code generation\"\"\"
    raise NotImplementedError("Code generation failed - please try again")"""
