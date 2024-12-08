"""
Tests for the autonomous coding agent
"""
import pytest
import os
from ..coding_agent import CodingAgent, CodingTask

def test_agent_initialization():
    """Test that agent initializes properly with API key"""
    # Temporarily set API key for testing
    os.environ["DEEPSEQ_API_KEY"] = "test_key"
    agent = CodingAgent()
    assert agent.api_key == "test_key"
    assert len(agent.messages) == 1  # Should have system message
    
def test_agent_initialization_no_api_key():
    """Test that agent raises error without API key"""
    if "DEEPSEQ_API_KEY" in os.environ:
        del os.environ["DEEPSEQ_API_KEY"]
    with pytest.raises(ValueError):
        CodingAgent()

def test_add_message():
    """Test adding messages to agent conversation"""
    os.environ["DEEPSEQ_API_KEY"] = "test_key"
    agent = CodingAgent()
    
    agent.add_message("Test message", "human")
    assert len(agent.messages) == 2
    assert agent.messages[-1].content == "Test message"
    
    with pytest.raises(ValueError):
        agent.add_message("Invalid role", "invalid")

def test_coding_task_creation():
    """Test creating a coding task"""
    task = CodingTask(
        description="Create a function to add two numbers",
        requirements=["Take two integer inputs", "Return their sum"],
        test_requirements=["Test with positive numbers", "Test with negative numbers"]
    )
    assert task.description == "Create a function to add two numbers"
    assert len(task.requirements) == 2
    assert len(task.test_requirements) == 2
