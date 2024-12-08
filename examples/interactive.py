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
        print("Please set OPENAI_API_KEY environment variable")
        return
    
    print("🤖 CodeWeaver Agent Test Environment")
    print("\nEnter 'quit' to exit (or Ctrl+C)")
    
    try:
        while True:
            try:
                print("\nWhat would you like me to code? (description):")
                description = input("> ")
                
                if description.lower() == 'quit':
                    break
                    
                print("\nWhat programming language?")
                language = input("> ")
                
                if not description.strip() or not language.strip():
                    print("Invalid input. Please try again.")
                    continue
                    
                task = CodingTask(description=description, language=language)
                print("\nGenerating code...\n")
                
                try:
                    result = await agent.generate(task)
                    print("Generated Code:")
                    print("-" * 40)
                    print(result)
                    print("-" * 40)
                except Exception as e:
                    print(f"Error generating code: {e}")
                    
            except KeyboardInterrupt:
                print("\nInterrupted. Enter 'quit' to exit or continue with a new task.")
                continue
                
    except KeyboardInterrupt:
        print("\nExiting...")
    
    print("\nThanks for using CodeWeaver!")

if __name__ == "__main__":
    asyncio.run(main())
