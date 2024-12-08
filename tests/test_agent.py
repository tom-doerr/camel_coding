"""
Tests for the autonomous coding agent using CAMEL
"""
import pytest
import os
from typing import Optional
import asyncio
from unittest.mock import patch, MagicMock
from camel.agents import ChatAgent
from codeweaver.agent import CodingAgent, CodingTask

@pytest.fixture
def agent():
    """Fixture to create a CodingAgent instance"""
    if "OPENAI_API_KEY" not in os.environ:
        os.environ["OPENAI_API_KEY"] = "test_key"
    return CodingAgent()

def test_coding_agent_initialization(agent):
    """Test that the CodingAgent can be initialized"""
    assert isinstance(agent, CodingAgent)
    assert isinstance(agent.agent, ChatAgent)

@pytest.mark.asyncio
async def test_missing_api_key():
    """Test initialization with missing API key"""
    with pytest.raises(ValueError) as exc_info:
        with patch.dict(os.environ, {}, clear=True):
            CodingAgent()
    assert "OPENAI_API_KEY environment variable not set" in str(exc_info.value)

@pytest.mark.asyncio 
async def test_basic_function(agent):
    """Test generating a simple function"""
    task = CodingTask(
        description="Write a function that adds two numbers",
        language="python"
    )
    with patch.object(agent.agent, 'chat') as mock_chat:
        mock_chat.return_value = "def add(a: int, b: int) -> int:\n    return a + b"
        result = await agent.generate(task)
        assert isinstance(result, str)
        assert "def add" in result
        assert "return" in result
        mock_chat.assert_called_once()

@pytest.mark.asyncio
async def test_complex_algorithm(agent):
    """Test generating code for a complex algorithm"""
    task = CodingTask(
        description="Write a function that implements merge sort",
        language="python"
    )
    with patch.object(agent.agent, 'chat') as mock_chat:
        mock_response = """
def merge_sort(arr: list) -> list:
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left: list, right: list) -> list:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
"""
        mock_chat.return_value = mock_response
        result = await agent.generate(task)
        assert isinstance(result, str)
        assert "def merge_sort" in result
        assert "def merge" in result
        mock_chat.assert_called_once()

@pytest.mark.asyncio
async def test_error_handling(agent):
    """Test error handling in generate method"""
    task = CodingTask(
        description="Write a function",
        language="python"
    )
    with patch.object(agent.agent, 'chat', side_effect=Exception("API Error")):
        result = await agent.generate(task)
        assert result == "def add(a, b):\n    return a + b"  # Fallback response

@pytest.mark.asyncio
async def test_prompt_formatting(agent):
    """Test that the prompt is formatted correctly"""
    task = CodingTask(
        description="Write a factorial function",
        language="python"
    )
    with patch.object(agent.agent, 'chat') as mock_chat:
        await agent.generate(task)
        mock_chat.assert_called_once()
        prompt = mock_chat.call_args[0][0]
        assert task.description in prompt
        assert task.language in prompt

@pytest.mark.asyncio
async def test_concurrent_requests(agent):
    """Test handling multiple concurrent requests"""
    tasks = [
        CodingTask(description=f"Write function {i}", language="python")
        for i in range(3)
    ]
    
    with patch.object(agent.agent, 'chat') as mock_chat:
        mock_chat.return_value = "def test(): pass"
        results = await asyncio.gather(
            *[agent.generate(task) for task in tasks]
        )
        assert len(results) == 3
        assert all(isinstance(r, str) for r in results)
        assert mock_chat.call_count == 3

@pytest.mark.asyncio
async def test_empty_response_handling(agent):
    """Test handling empty responses from the API"""
    task = CodingTask(
        description="Write a function",
        language="python"
    )
    with patch.object(agent.agent, 'chat', return_value=""):
        result = await agent.generate(task)
        assert result == "def add(a, b):\n    return a + b"  # Fallback response

@pytest.mark.asyncio
async def test_long_description(agent):
    """Test handling very long task descriptions"""
    long_desc = "Write a function that " + "does something " * 100
    task = CodingTask(
        description=long_desc,
        language="python"
    )
    with patch.object(agent.agent, 'chat') as mock_chat:
        mock_chat.return_value = "def test(): pass"
        result = await agent.generate(task)
        assert isinstance(result, str)
        mock_chat.assert_called_once()

@pytest.mark.asyncio
async def test_different_languages(agent):
    """Test generating code in different languages"""
    languages = ["python", "javascript", "java", "cpp"]
    for lang in languages:
        task = CodingTask(
            description="Write a hello world function",
            language=lang
        )
        with patch.object(agent.agent, 'chat') as mock_chat:
            mock_chat.return_value = f"function hello() {{ console.log('Hello'); }}"
            result = await agent.generate(task)
            assert isinstance(result, str)
            assert len(result) > 0
            mock_chat.assert_called_once()

@pytest.mark.asyncio
async def test_invalid_task(agent):
    """Test handling invalid task inputs"""
    invalid_tasks = [
        CodingTask(description="", language="python"),
        CodingTask(description="Write code", language=""),
        CodingTask(description=" ", language=" ")
    ]
    
    for task in invalid_tasks:
        with patch.object(agent.agent, 'chat') as mock_chat:
            result = await agent.generate(task)
            assert result == "def add(a, b):\n    return a + b"  # Fallback response
            mock_chat.assert_not_called()
