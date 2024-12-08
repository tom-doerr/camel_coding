"""
Demo script showing CAMEL EmbodiedAgent capabilities
"""
from camel.agents import EmbodiedAgent
from camel.messages import BaseMessage
from camel.generators import SystemMessageGenerator
from camel.types import RoleType

def run_embodied_demo():
    """Run demonstration of EmbodiedAgent capabilities"""
    print("\nCAMEL EmbodiedAgent Demo")
    print("-" * 40)
    
    # Initialize system message generator
    sys_msg_gen = SystemMessageGenerator()
    
    # Create role and task metadata
    role = "Python Expert"
    task = "Writing and reviewing Python code"
    meta_dict = {"role": role, "task": task}
    role_tuple = (role, RoleType.EMBODIMENT)
    
    # Generate system message
    system_message = sys_msg_gen.from_dict(meta_dict=meta_dict, role_tuple=role_tuple)
    
    print("\nInitializing agent with system message:")
    print(f"Role: {role}")
    print(f"Task: {task}")
    
    # Initialize the embodied agent
    agent = EmbodiedAgent(
        system_message=system_message,
        verbose=True
    )
    
    # Test cases to demonstrate capabilities
    test_cases = [
        {
            "name": "Code Review",
            "message": """
Please review this code:

def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)
"""
        },
        {
            "name": "Code Improvement",
            "message": """
How can we make this code better?

def sort_list(items):
    n = len(items)
    for i in range(n):
        for j in range(n-1):
            if items[j] > items[j+1]:
                items[j], items[j+1] = items[j+1], items[j]
    return items
"""
        },
        {
            "name": "Documentation",
            "message": "How should we document Python functions following best practices?"
        }
    ]
    
    # Run each test case
    for test in test_cases:
        try:
            print(f"\nRunning: {test['name']}")
            print("-" * 20)
            
            # Create user message
            user_msg = BaseMessage.make_user_message(
                role_name="Developer",
                content=test['message']
            )
            
            # Get agent's response
            response = agent.step(user_msg)
            
            print("\nAgent Response:")
            print("-" * 15)
            print(response.content)
            
        except Exception as e:
            print(f"Error in {test['name']}: {str(e)}")

def main():
    """Main function"""
    try:
        run_embodied_demo()
    except Exception as e:
        print(f"Demo failed: {str(e)}")
        print("\nMake sure OPENAI_API_KEY is set!")

if __name__ == "__main__":
    main()
