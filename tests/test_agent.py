"""
Tests for the autonomous coding agent
"""
import pytest
from codeweaver.agent import CodingAgent, CodingTask

def test_coding_agent_initialization():
    """Test that the CodingAgent can be initialized"""
    agent = CodingAgent()
    assert isinstance(agent, CodingAgent)

@pytest.mark.asyncio 
async def test_coding_agent_generate():
    """Test that the CodingAgent can generate code"""
    agent = CodingAgent()
    task = CodingTask(
        description="Write a function that adds two numbers",
        language="python"
    )
    result = await agent.generate(task)
    assert isinstance(result, str)
