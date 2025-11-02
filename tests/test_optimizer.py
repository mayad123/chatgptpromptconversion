"""
Tests for the prompt optimizer.
"""

import pytest
from agent.optimizer import PromptOptimizer


class TestPromptOptimizer:
    """Test cases for PromptOptimizer."""
    
    def test_optimizer_initialization(self):
        """Test optimizer can be initialized."""
        optimizer = PromptOptimizer()
        assert optimizer is not None
        assert optimizer.parser is not None
        assert optimizer.validator is not None
    
    def test_simple_optimization(self):
        """Test basic prompt optimization."""
        optimizer = PromptOptimizer()
        input_text = "Write me a story about a robot"
        result = optimizer.optimize(input_text)
        
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0
        assert "Task:" in result or "task" in result.lower()
    
    def test_optimization_with_context(self):
        """Test optimization with context."""
        optimizer = PromptOptimizer()
        input_text = "Given that I'm a beginner, explain machine learning"
        result = optimizer.optimize(input_text)
        
        assert result is not None
        assert "machine learning" in result.lower()


if __name__ == "__main__":
    pytest.main([__file__])

