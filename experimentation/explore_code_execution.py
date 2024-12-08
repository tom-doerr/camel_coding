"""
Script to explore CAMEL code execution toolkit capabilities
"""
from camel.toolkits.code_execution import (
    CodeExecutionToolkit,
    DockerInterpreter,
    InternalPythonInterpreter,
    JupyterKernelInterpreter,
    SubprocessInterpreter
)

def explore_interpreters():
    """Explore available code execution interpreters"""
    interpreters = {
        "Docker": DockerInterpreter,
        "Internal Python": InternalPythonInterpreter,
        "Jupyter Kernel": JupyterKernelInterpreter,
        "Subprocess": SubprocessInterpreter
    }
    
    print("\nCAMEL Code Execution Interpreters:")
    print("-" * 40)
    
    for name, interpreter_class in interpreters.items():
        print(f"\n{name} Interpreter:")
        print("-" * 20)
        
        # Get supported code types
        if hasattr(interpreter_class, 'supported_code_types'):
            supported = interpreter_class.supported_code_types()
            print(f"Supported code types: {', '.join(supported)}")
            
        # Show initialization parameters
        init_params = interpreter_class.__init__.__annotations__
        if init_params:
            print("\nInitialization parameters:")
            for param, param_type in init_params.items():
                if param != 'return':
                    print(f"- {param}: {param_type}")
                    
def explore_toolkit():
    """Explore CodeExecutionToolkit capabilities"""
    print("\nCodeExecutionToolkit Details:")
    print("-" * 40)
    
    # Initialize toolkit with different sandbox types
    sandbox_types = ["docker", "jupyter", "python", "subprocess"]
    
    for sandbox in sandbox_types:
        try:
            toolkit = CodeExecutionToolkit(sandbox=sandbox)
            print(f"\nSandbox type: {sandbox}")
            
            # Get available tools
            tools = toolkit.get_tools()
            print(f"Available tools: {len(tools)}")
            for tool in tools:
                print(f"- {tool.name}: {tool.__doc__ if tool.__doc__ else 'No documentation'}")
                
        except Exception as e:
            print(f"Error with {sandbox} sandbox: {str(e)}")

def main():
    """Main function"""
    try:
        explore_interpreters()
        explore_toolkit()
    except Exception as e:
        print(f"Error exploring code execution: {e}")

if __name__ == "__main__":
    main()
