"""
Tests for the autonomous coding agent
"""
import pytest
import os
from unittest.mock import patch, MagicMock
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
async def test_basic_function():
    """Test generating a simple function"""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
        agent = CodingAgent()
        task = CodingTask(
            description="Write a function that adds two numbers",
            language="python"
        )
        with patch.object(agent.client.chat.completions, 'create') as mock_create:
            mock_create.return_value.choices[0].message.content = "def add(a: int, b: int) -> int:\n    return a + b"
            result = await agent.generate(task)
            assert isinstance(result, str)
            assert "def add" in result
            assert "return" in result
            mock_create.assert_called_once()

@pytest.mark.asyncio
async def test_invalid_task():
    """Test handling invalid task inputs"""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
        agent = CodingAgent()
        invalid_tasks = [
            CodingTask(description="", language="python"),
            CodingTask(description="Write code", language=""),
            CodingTask(description=" ", language=" ")
        ]
        
        for task in invalid_tasks:
            with patch.object(agent.client.chat.completions, 'create') as mock_create:
                result = await agent.generate(task)
                assert result == "def add(a, b):\n    return a + b"  # Fallback response
                mock_create.assert_not_called()
