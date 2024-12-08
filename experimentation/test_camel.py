"""
Direct test of CAMEL API integration
"""
import os
from camel.societies import RolePlaying
from colorama import Fore, init

# Initialize colorama
init()

def test_camel():
    """Test direct communication with CAMEL"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        return

    # Define roles and task
    user_role = "Python Developer"
    assistant_role = "Code Reviewer"
    task = "Review a Python function that calculates factorial"

    try:
        # Initialize role-playing session
        session = RolePlaying(
            user_role_name=user_role,
            assistant_role_name=assistant_role,
            task_prompt=task,
            with_task_specify=True
        )
        
        # Print initial setup
        print(Fore.GREEN + f"\nAssistant System Message:\n{session.assistant_sys_msg}\n")
        print(Fore.BLUE + f"User System Message:\n{session.user_sys_msg}\n")
        print(Fore.YELLOW + f"Original Task:\n{task}\n")
        print(Fore.CYAN + f"Specified Task:\n{session.specified_task_prompt}\n")
        
        # Run conversation
        chat_turns = 5
        for _ in range(chat_turns):
            # Get assistant's response
            assistant_response = session.step(assistant_role)
            print(Fore.GREEN + "Assistant:\n" + f"{assistant_response.content}\n")
            
            # Get user's response
            user_response = session.step(user_role)
            print(Fore.BLUE + "User:\n" + f"{user_response.content}\n")
            
            # Check if task is complete
            if "CAMEL_TASK_DONE" in assistant_response.content:
                break
                
    except Exception as e:
        print(f"CAMEL Error: {str(e)}")

if __name__ == "__main__":
    test_camel()
