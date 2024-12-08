"""
Interactive testing environment for CodeWeaver
"""
import asyncio
import os
from codeweaver.agent import CodingAgent, CodingTask

async def main():
    # Get model selection
    print("\nSelect model to use:")
    print("1. OpenAI (default)")
    print("2. DeepSeek")
    choice = input("> ").strip()
    
    model = "openai" if choice != "2" else "deepseek"
    
    try:
        agent = CodingAgent(model=model)
    except ValueError as e:
        print(f"Error: {e}")
        if model == "openai":
            print("Please set OPENAI_API_KEY environment variable")
        else:
            print("Please set DEEPSEEK_API_KEY environment variable")
        return
    
    print("🤖 CodeWeaver Agent Test Environment")
    print("\nEnter 'quit' to exit (or Ctrl+C)")
    
    try:
        while True:
            try:
                print("\nWhat would you like me to code? (or 'quit' to exit):")
                description = input("> ")
                
                if description.lower() == 'quit':
                    break
                    
                if not description.strip():
                    print("Invalid input. Please try again.")
                    continue
                    
                task = CodingTask(description=description)
                print("\nGenerating code...\n")
                
                result = await agent.generate(task)
                
                if result:
                    print("Generated Code:")
                    print("-" * 40)
                    print(result)
                    print("-" * 40)
                    
                    # Ask if user wants to save the code
                    print("\nWould you like to save this code to a file? [y/N]:")
                    save = input("> ").lower().strip()
                    if save == 'y':
                        print("Enter filename (default: output.py):")
                        filename = input("> ").strip() or "output.py"
                        try:
                            with open(filename, 'w') as f:
                                f.write(result)
                            print(f"Code saved to {filename}")
                        except Exception as e:
                            print(f"Error saving file: {e}")
                    
            except KeyboardInterrupt:
                print("\nInterrupted. Enter 'quit' to exit or continue with a new task.")
                continue
                
    except KeyboardInterrupt:
        print("\nExiting...")
    
    print("\nThanks for using CodeWeaver!")

if __name__ == "__main__":
    asyncio.run(main())
