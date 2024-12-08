"""
Demo script showing Docker-based code execution using CAMEL toolkit
"""
import time
from camel.toolkits.code_execution import DockerInterpreter

def run_docker_demo():
    """Run example code in Docker container"""
    print("\nCAMEL Docker Code Execution Demo")
    print("-" * 40)
    
    # Initialize Docker interpreter
    interpreter = DockerInterpreter(
        require_confirm=False,  # Don't require confirmation for demo
        print_stdout=True,      # Show stdout from container
        print_stderr=True       # Show stderr from container
    )
    
    # Test cases to demonstrate different aspects
    test_cases = [
        {
            "name": "Basic Python",
            "code": """
print("Hello from Docker container!")
x = 42
print(f"x = {x}")
""",
            "lang": "python"
        },
        {
            "name": "File Operations",
            "code": """
with open('test.txt', 'w') as f:
    f.write('Hello from container!')
    
with open('test.txt', 'r') as f:
    content = f.read()
    print(f"File contains: {content}")
""",
            "lang": "python"
        },
        {
            "name": "System Commands",
            "code": """
import os
print("Current directory:", os.getcwd())
print("\nDirectory contents:")
print(os.listdir())
""",
            "lang": "python"
        },
        {
            "name": "Shell Commands",
            "code": """
echo "Running in container"
pwd
ls -la
""",
            "lang": "bash"
        }
    ]
    
    # Run each test case
    for test in test_cases:
        try:
            print(f"\nRunning: {test['name']}")
            print("-" * 20)
            
            # Execute code in container
            start_time = time.time()
            result = interpreter.run(
                code=test['code'].strip(),
                code_type=test['lang']
            )
            end_time = time.time()
            
            # Show execution time
            print(f"\nExecution time: {end_time - start_time:.2f} seconds")
            
            if result.stderr:
                print("\nErrors/Warnings:")
                print(result.stderr)
                
        except Exception as e:
            print(f"Error running {test['name']}: {str(e)}")
            
def main():
    """Main function"""
    try:
        run_docker_demo()
    except Exception as e:
        print(f"Docker demo failed: {str(e)}")
        print("\nMake sure Docker is installed and running!")

if __name__ == "__main__":
    main()
