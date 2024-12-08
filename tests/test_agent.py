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

def test_missing_api_key():
    """Test initialization with missing API key"""
    with pytest.raises(ValueError) as exc_info:
        with patch.dict(os.environ, {}, clear=True):
            CodingAgent()
    assert "OPENAI_API_KEY environment variable not set" in str(exc_info.value)

def test_agent_initialization():
    """Test agent initialization with tools"""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
        agent = CodingAgent()
        assert agent.system_message is not None
        assert agent.agent is not None

def test_basic_function():
    """Test generating a simple function"""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
        agent = CodingAgent()
        task = CodingTask(description="Write a function that adds two numbers")
        
        mock_response = MagicMock()
        mock_response.content = "def add(a: int, b: int) -> int:\n    return a + b"
        
        with patch.object(agent.agent, 'step', new_callable=AsyncMock) as mock_step:
            mock_step.return_value = mock_response
            result = agent.generate(task)
            
            assert isinstance(result, str)
            assert "def add" in result
            assert "return" in result
            mock_step.assert_called_once()

def test_invalid_task():
    """Test handling invalid task inputs"""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
        agent = CodingAgent()
        invalid_tasks = [
            CodingTask(description=""),
            CodingTask(description=" ")
        ]
        
        for task in invalid_tasks:
            with patch.object(agent.agent, 'step', new_callable=AsyncMock) as mock_step:
                result = agent.generate(task)
                assert result == "def add(a, b):\n    return a + b"  # Fallback response
                mock_step.assert_not_called()

def test_empty_response():
    """Test handling empty response from agent"""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
        agent = CodingAgent()
        task = CodingTask(description="Write a simple function")
        
        mock_response = MagicMock()
        mock_response.content = ""
        
        with patch.object(agent.agent, 'step', new_callable=AsyncMock) as mock_step:
            mock_step.return_value = mock_response
            result = agent.generate(task)
            assert "error_response" in result
            assert "NotImplementedError" in result

def test_code_extraction():
    """Test extracting code from CAMEL response"""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
        agent = CodingAgent()
        task = CodingTask(description="show time")
        
        # Test response with "> Code:" marker
        mock_response = MagicMock()
        mock_response.content = """
[35m> Explanation:
Some explanation here
[35m> Code:
def show_time():
    return "12:00"
2024-12-08 INFO - Some debug info"""
        
        with patch.object(agent.agent, 'step', new_callable=AsyncMock) as mock_step:
            mock_step.return_value = mock_response
            result = agent.generate(task)
            assert "def show_time" in result
            assert "INFO -" not in result
            assert "Explanation" not in result
            
        # Test response without marker but with debug info
        mock_response.content = """def another_func():
    pass
2024-12-08 INFO - Debug info"""
        
        with patch.object(agent.agent, 'step', new_callable=AsyncMock) as mock_step:
            mock_step.return_value = mock_response
            result = agent.generate(task)
            assert "def another_func" in result
            assert "INFO -" not in result

def test_error_response():
    """Test error response format"""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
        agent = CodingAgent()
        task = CodingTask(description="show time")
        
        # Test completely empty response
        mock_response = MagicMock()
        mock_response.content = ""
        
        with patch.object(agent.agent, 'step', new_callable=AsyncMock) as mock_step:
            mock_step.return_value = mock_response
            result = agent.generate(task)
            assert "error_response" in result
            assert "NotImplementedError" in result
            
        # Test invalid response format
        mock_response.content = "Not a valid code block"
        with patch.object(agent.agent, 'step', new_callable=AsyncMock) as mock_step:
            mock_step.return_value = mock_response
            result = agent.generate(task)
            assert "error_response" in result

def test_complex_tasks():
    """Test generating code for more complex tasks"""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
        agent = CodingAgent()
        tasks = [
            "Write a function to calculate fibonacci numbers",
            "Create a binary search implementation",
            "Make a simple stack data structure"
        ]
        
        mock_response = MagicMock()
        mock_response.content = """[35m> Code:
def sample():
    pass"""
        
        for description in tasks:
            task = CodingTask(description=description)
            with patch.object(agent.agent, 'step', new_callable=AsyncMock) as mock_step:
                mock_step.return_value = mock_response
                result = agent.generate(task)
                assert isinstance(result, str)
                assert "def sample" in result
