"""
Script to inspect DockerInterpreter initialization parameters
"""
from inspect import signature, Parameter
from camel.toolkits.code_execution import DockerInterpreter

def inspect_docker_interpreter():
    """Inspect DockerInterpreter class parameters"""
    print("\nDockerInterpreter Parameters:")
    print("-" * 40)
    
    sig = signature(DockerInterpreter)
    
    for name, param in sig.parameters.items():
        print(f"\nParameter: {name}")
        print(f"Default: {param.default if param.default != Parameter.empty else 'Required'}")
        print(f"Kind: {param.kind}")
        
        # Get annotation info if available
        if param.annotation != Parameter.empty:
            print(f"Type: {param.annotation}")
            
if __name__ == "__main__":
    inspect_docker_interpreter()
