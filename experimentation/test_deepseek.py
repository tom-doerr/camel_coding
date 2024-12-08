"""
Direct test of DeepSeek API integration
"""
import os
import asyncio
from openai import AsyncOpenAI

async def test_deepseek_api():
    """Test direct communication with DeepSeek API"""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("Error: DEEPSEEK_API_KEY environment variable not set")
        return

    client = AsyncOpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com/v1"
    )
    
    try:
        response = await client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful coding assistant."},
                {"role": "user", "content": "Write a simple Python function that adds two numbers."}
            ],
            temperature=0.7,
            max_tokens=1000,
            stream=False
        )
        
        print("API Response:")
        print("-" * 40)
        print(response.choices[0].message.content)
        print("-" * 40)
        
    except Exception as e:
        print(f"API Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_deepseek_api())
