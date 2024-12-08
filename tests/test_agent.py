"""
Tests for the autonomous coding agent using DeepSeek
"""
import pytest
import os
from typing import Optional
from codeweaver.agent import CodingAgent, CodingTask

@pytest.fixture
def agent():
    """Fixture to create a CodingAgent instance"""
    if "DEEPSEEK_API_KEY" not in os.environ:
        os.environ["DEEPSEEK_API_KEY"] = "test_key"
    return CodingAgent()

def test_coding_agent_initialization(agent):
    """Test that the CodingAgent can be initialized"""
    assert isinstance(agent, CodingAgent)
    assert agent.api_key is not None

@pytest.mark.asyncio 
async def test_basic_function(agent):
    """Test generating a simple function"""
    task = CodingTask(
        description="Write a function that adds two numbers",
        language="python",
        test_requirements="Include tests for positive, negative and zero numbers"
    )
    result = await agent.generate(task)
    assert isinstance(result, str)
    assert "def" in result
    assert "return" in result
    assert "def test_" in result.lower()

@pytest.mark.asyncio
async def test_complex_algorithm(agent):
    """Test generating code for a complex algorithm"""
    task = CodingTask(
        description="Write a function that implements merge sort",
        language="python",
        test_requirements="Include tests for: empty list, single item, already sorted, reverse sorted"
    )
    result = await agent.generate(task)
    assert isinstance(result, str)
    assert "def merge_sort" in result.lower()
    assert "def test_" in result.lower()

@pytest.mark.asyncio
async def test_error_handling(agent):
    """Test generating code with error handling"""
    task = CodingTask(
        description="Write a function that reads a JSON file and returns its contents",
        language="python",
        test_requirements="Test file not found and invalid JSON scenarios"
    )
    result = await agent.generate(task)
    assert isinstance(result, str)
    assert "try:" in result
    assert "except" in result
    assert "def test_" in result.lower()

@pytest.mark.asyncio
async def test_different_language(agent):
    """Test generating code in a different language"""
    task = CodingTask(
        description="Write a function that checks if a string is a palindrome",
        language="javascript",
        test_requirements="Test empty string, single char, valid palindrome, invalid palindrome"
    )
    result = await agent.generate(task)
    assert isinstance(result, str)
    assert "function" in result.lower()
    assert "test" in result.lower()

@pytest.mark.asyncio
async def test_api_failure(agent):
    """Test handling of API failures"""
    task = CodingTask(
        description="This should fail",
        language="python"
    )
    # Invalidate the API key to force failure
    agent.api_key = "invalid_key"
    result = await agent.generate(task)
    assert result is None
