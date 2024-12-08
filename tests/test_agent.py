"""
Tests for the autonomous coding agent
"""
import pytest
import os
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

@pytest.mark.asyncio 
async def test_coding_agent_generate(agent):
    """Test that the CodingAgent can generate code"""
    task = CodingTask(
        description="Write a function that adds two numbers",
        language="python"
    )
    result = await agent.generate(task)
    assert isinstance(result, str)
    assert "def" in result  # Basic check that we got some code
    assert "return" in result

@pytest.mark.asyncio
async def test_complex_task(agent):
    """Test generating code for a more complex task"""
    task = CodingTask(
        description="Write a function that calculates the fibonacci sequence",
        language="python"
    )
    result = await agent.generate(task)
    assert isinstance(result, str)
    assert "def" in result
    assert "fibonacci" in result.lower()
