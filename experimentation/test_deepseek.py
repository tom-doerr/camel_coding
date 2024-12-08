"""
Direct test of DeepSeek API integration
"""
import os
import asyncio
from openai import AsyncOpenAI

async def test_deepseek_api():
    """Test direct communication with DeepSeek API"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        return

    client = AsyncOpenAI(api_key=api_key)
    
    try:
        response = await client.chat.completions.create(
            model="gpt-4",  # or your specific DeepSeek model
            messages=[
                {"role": "system", "content": "You are a helpful coding assistant."},
                {"role": "user", "content": "Write a simple Python function that adds two numbers."}
            ]
        )
        
        print("API Response:")
        print("-" * 40)
        print(response.choices[0].message.content)
        print("-" * 40)
        
    except Exception as e:
        print(f"API Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_deepseek_api())
