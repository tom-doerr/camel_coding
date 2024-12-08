"""
Tests for the autonomous coding agent using CAMEL framework
"""
import pytest
import os
from unittest.mock import patch, MagicMock, AsyncMock
from camel.messages import BaseMessage
from codeweaver.agent import CodingAgent, CodingTask

@pytest.fixture
def mock_env():
    """Fixture to set up test environment variables"""
    original_key = os.environ.get("OPENAI_API_KEY")
    yield
    if original_key:
        os.environ["OPENAI_API_KEY"] = original_key
    else:
        os.environ.pop("OPENAI_API_KEY", None)

@pytest.mark.asyncio
async def test_missing_api_key():
    """Test initialization with missing API key"""
    with pytest.raises(ValueError) as exc_info:
        with patch.dict(os.environ, {}, clear=True):
            CodingAgent()
    assert "OPENAI_API_KEY environment variable not set" in str(exc_info.value)

@pytest.mark.asyncio
async def test_agent_initialization():
    """Test agent initialization with tools"""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
        agent = CodingAgent()
        assert agent.system_message is not None
        assert agent.agent is not None

@pytest.mark.asyncio
async def test_basic_function():
    """Test generating a simple function"""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
        agent = CodingAgent()
        task = CodingTask(description="Write a function that adds two numbers")
        
        mock_response = MagicMock()
        mock_response.content = "def add(a: int, b: int) -> int:\n    return a + b"
        
        with patch.object(agent.agent, 'step', new_callable=AsyncMock) as mock_step:
            mock_step.return_value = mock_response
            result = await agent.generate(task)
            
            assert isinstance(result, str)
            assert "def add" in result
            assert "return" in result
            mock_step.assert_called_once()

@pytest.mark.asyncio
async def test_invalid_task():
    """Test handling invalid task inputs"""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
        agent = CodingAgent()
        invalid_tasks = [
            CodingTask(description=""),
            CodingTask(description=" ")
        ]
        
        for task in invalid_tasks:
            with patch.object(agent.agent, 'step', new_callable=AsyncMock) as mock_step:
                result = await agent.generate(task)
                assert result == "def add(a, b):\n    return a + b"  # Fallback response
                mock_step.assert_not_called()

@pytest.mark.asyncio
async def test_empty_response():
    """Test handling empty response from agent"""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
        agent = CodingAgent()
        task = CodingTask(description="Write a simple function")
        
        mock_response = MagicMock()
        mock_response.content = ""
        
        with patch.object(agent.agent, 'step', new_callable=AsyncMock) as mock_step:
            mock_step.return_value = mock_response
            result = await agent.generate(task)
            assert result == "def add(a, b):\n    return a + b"  # Fallback response

@pytest.mark.asyncio
async def test_complex_tasks():
    """Test generating code for more complex tasks"""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
        agent = CodingAgent()
        tasks = [
            "Write a function to calculate fibonacci numbers",
            "Create a binary search implementation",
            "Make a simple stack data structure"
        ]
        
        mock_response = MagicMock()
        mock_response.content = "def sample():\n    pass"
        
        for description in tasks:
            task = CodingTask(description=description)
            with patch.object(agent.agent, 'step', new_callable=AsyncMock) as mock_step:
                mock_step.return_value = mock_response
                result = await agent.generate(task)
                assert isinstance(result, str)
                assert len(result) > 0
