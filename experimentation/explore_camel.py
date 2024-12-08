"""
Script to explore CAMEL tools and capabilities
"""
import os
import inspect
from camel.agents import EmbodiedAgent
from camel.messages import BaseMessage
from camel.generators import SystemMessageGenerator
from camel.types import RoleType
from camel import toolkits
from camel.toolkits import code_execution

def list_available_tools():
    """List available CAMEL tools and capabilities"""
    print("\nCAMEL Tools & Components:")
    print("-" * 40)
    
    # Initialize test agent to explore capabilities
    agent = EmbodiedAgent(
        system_message="Test system message",
        verbose=True
    )
    
    # Get available actions
    print("\nAvailable Actions:")
    if hasattr(agent, 'action_space'):
        for action in agent.action_space:
            print(f"- {action}")
    else:
        print("No action_space attribute found")
        
    # List message types
    print("\nMessage Types:")
    print("- BaseMessage")
    print("- SystemMessage")
    print("- UserMessage")
    print("- AssistantMessage")
    
    # List agent types
    print("\nAgent Types:")
    print("- ChatAgent")
    print("- EmbodiedAgent")
    print("- RolePlayingAgent")
    
    # List generators
    print("\nGenerators:")
    print("- SystemMessageGenerator")
    print("- UserMessageGenerator")
    print("- AssistantMessageGenerator")
    
    # List role types
    print("\nRole Types:")
    for role_type in RoleType:
        print(f"- {role_type.name}")
        
    # Explore toolkits
    print("\nAvailable Toolkits:")
    toolkit_members = inspect.getmembers(toolkits)
    for name, obj in toolkit_members:
        if inspect.ismodule(obj):
            print(f"\n- {name}:")
            module_members = inspect.getmembers(obj)
            for member_name, member_obj in module_members:
                if inspect.isclass(member_obj):
                    print(f"  - Class: {member_name}")
                    # Special handling for code execution toolkit
                    if name == "code_execution" and hasattr(member_obj, "__doc__"):
                        doc = member_obj.__doc__
                        if doc:
                            print(f"    Documentation: {doc.strip()}")
                        # List methods
                        methods = inspect.getmembers(member_obj, 
                            predicate=lambda x: inspect.isfunction(x) or inspect.ismethod(x))
                        if methods:
                            print("    Methods:")
                            for method_name, method in methods:
                                if not method_name.startswith("_"):  # Skip private methods
                                    method_doc = method.__doc__ or "No documentation"
                                    print(f"      - {method_name}: {method_doc.strip()}")
                elif inspect.isfunction(member_obj):
                    print(f"  - Function: {member_name}")
                    if member_obj.__doc__:
                        print(f"    Documentation: {member_obj.__doc__.strip()}")

def main():
    """Main function"""
    try:
        list_available_tools()
    except Exception as e:
        print(f"Error exploring CAMEL tools: {e}")

if __name__ == "__main__":
    main()
