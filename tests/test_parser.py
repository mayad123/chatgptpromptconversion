"""
Tests for the natural language parser.
"""

import pytest
from agent.parser import NaturalLanguageParser


class TestNaturalLanguageParser:
    """Test cases for NaturalLanguageParser."""
    
    def test_parser_initialization(self):
        """Test parser can be initialized."""
        parser = NaturalLanguageParser()
        assert parser is not None
    
    def test_intent_extraction(self):
        """Test intent extraction from text."""
        parser = NaturalLanguageParser()
        
        test_cases = [
            ("Write me a story", "story"),
            ("Create a Python script", "Python script"),
            ("Explain quantum physics", "quantum physics"),
        ]
        
        for text, expected_contains in test_cases:
            result = parser.parse(text)
            assert "intent" in result
            assert expected_contains.lower() in result["intent"].lower()
    
    def test_requirement_extraction(self):
        """Test requirement extraction."""
        parser = NaturalLanguageParser()
        
        text = "Write code that should be efficient and must include error handling"
        result = parser.parse(text)
        
        assert "requirements" in result
        assert isinstance(result["requirements"], list)
    
    def test_full_parse_structure(self):
        """Test that parse returns correct structure."""
        parser = NaturalLanguageParser()
        result = parser.parse("Write a blog post about AI")
        
        assert "intent" in result
        assert "context" in result
        assert "requirements" in result
        assert "output_format" in result
        assert "original_text" in result


if __name__ == "__main__":
    pytest.main([__file__])

