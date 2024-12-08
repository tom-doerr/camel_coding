"""
Tests for different model backends
"""
import pytest
import os
from unittest.mock import patch, MagicMock, AsyncMock
from codeweaver.agent import CodingAgent, CodingTask

def test_model_selection():
    """Test selecting different models"""
    # Test OpenAI
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
        agent = CodingAgent(model="openai")
        assert agent.model == "openai"
        
    # Test DeepSeek
    with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test_key"}):
        agent = CodingAgent(model="deepseek")
        assert agent.model == "deepseek"
        
    # Test invalid model
    with pytest.raises(ValueError) as exc_info:
        CodingAgent(model="invalid")
    assert "Unsupported model" in str(exc_info.value)

def test_missing_api_keys():
    """Test handling of missing API keys"""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError) as exc_info:
            CodingAgent(model="openai")
        assert "OPENAI_API_KEY" in str(exc_info.value)
        
        with pytest.raises(ValueError) as exc_info:
            CodingAgent(model="deepseek")
        assert "DEEPSEEK_API_KEY" in str(exc_info.value)
