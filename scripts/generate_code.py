"""
Script to generate code using CAMEL agent and save to outputs directory
"""
import os
import sys
from pathlib import Path
from codeweaver.agent import CodingAgent, CodingTask

def main():
    """Main function to generate and save code"""
    # Ensure outputs directory exists
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    
    # Get the coding task from command line argument
    if len(sys.argv) < 2:
        print("Usage: python generate_code.py \"<coding task description>\"")
        sys.exit(1)
        
    task_description = sys.argv[1]
    
    try:
        # Initialize the agent
        agent = CodingAgent()
        
        # Create the task
        task = CodingTask(description=task_description)
        
        # Generate the code
        print(f"\nGenerating code for: {task_description}")
        print("-" * 40)
        
        code = agent.generate(task)
        
        if code:
            # Create filename from task description
            filename = task_description.lower()
            filename = "".join(c if c.isalnum() else "_" for c in filename)
            filename = filename[:30] + ".py"  # Truncate if too long
            
            # Full path in outputs directory
            output_path = output_dir / filename
            
            # Save the code
            with open(output_path, "w") as f:
                f.write(code)
                
            print(f"\nCode generated successfully!")
            print(f"Saved to: {output_path}")
            print("\nGenerated Code:")
            print("-" * 40)
            print(code)
            print("-" * 40)
            
        else:
            print("Error: No code was generated")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
