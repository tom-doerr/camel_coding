"""
Interactive testing environment for CodeWeaver
"""
import asyncio
import os
from codeweaver.agent import CodingAgent, CodingTask

async def main():
    try:
        agent = CodingAgent()
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set DEEPSEEK_API_KEY environment variable")
        return
    
    # Example task
    task = CodingTask(
        description="Write a function that calculates the fibonacci sequence",
        language="python"
    )

    print("🤖 CodeWeaver Agent Test Environment")
    print("\nTask:", task.description)
    print("\nGenerating code...\n")

    result = await agent.generate(task)
    print("Generated Code:")
    print("-" * 40)
    print(result)
    print("-" * 40)

if __name__ == "__main__":
    asyncio.run(main())
