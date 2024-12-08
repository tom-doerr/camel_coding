"""
Interactive testing environment for CodeWeaver
"""
import asyncio
import os
from codeweaver.agent import CodingAgent, CodingTask

async def main():
    # Ensure API key is set
    if "DEEPSEQ_API_KEY" not in os.environ:
        print("Please set DEEPSEQ_API_KEY environment variable")
        return

    agent = CodingAgent()
    
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
