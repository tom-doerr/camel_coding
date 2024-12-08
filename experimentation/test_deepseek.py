"""
Test script for comparing OpenAI and DeepSeek model outputs
"""
import os
import asyncio
from codeweaver.agent import CodingAgent, CodingTask

def compare_models():
    """Compare outputs from different models"""
    # Test tasks
    tasks = [
        "Write a function to calculate the factorial of a number",
        "Create a function to check if a string is a palindrome",
        "Write a function to find the nth Fibonacci number"
    ]
    
    # Test with both models
    models = ["openai", "deepseek"]
    
    for model in models:
        print(f"\nTesting {model.upper()} model:")
        print("-" * 40)
        
        try:
            agent = CodingAgent(model=model)
            
            for task in tasks:
                print(f"\nTask: {task}")
                print("-" * 20)
                
                try:
                    result = agent.generate(CodingTask(description=task))
                    print("\nGenerated Code:")
                    print("-" * 40)
                    print(result)
                    print("-" * 40)
                except Exception as e:
                    print(f"Error generating code: {e}")
                
        except ValueError as e:
            print(f"Error: {e}")
            continue
            
if __name__ == "__main__":
    compare_models()
