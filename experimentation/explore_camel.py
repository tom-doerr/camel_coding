"""
Script to explore CAMEL tools and capabilities
"""
import os
from camel.agents import EmbodiedAgent
from camel.messages import BaseMessage
from camel.generators import SystemMessageGenerator
from camel.types import RoleType

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

def main():
    """Main function"""
    try:
        list_available_tools()
    except Exception as e:
        print(f"Error exploring CAMEL tools: {e}")

if __name__ == "__main__":
    main()
