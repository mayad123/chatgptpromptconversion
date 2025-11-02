"""
Configuration settings for the prompt optimization agent.
"""

import os
from typing import Dict

# Try to load environment variables from .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If python-dotenv is not installed, just use system environment variables
    pass


class Settings:
    """Configuration settings."""
    
    # API Settings (if using OpenAI API directly)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # Prompt optimization settings
    MAX_PROMPT_LENGTH = int(os.getenv("MAX_PROMPT_LENGTH", "4000"))
    MIN_PROMPT_LENGTH = int(os.getenv("MIN_PROMPT_LENGTH", "10"))
    
    # Optimization preferences
    PREFER_STRUCTURED = os.getenv("PREFER_STRUCTURED", "true").lower() == "true"
    INCLUDE_EXAMPLES = os.getenv("INCLUDE_EXAMPLES", "true").lower() == "true"
    
    # Output settings
    OUTPUT_FORMAT = os.getenv("OUTPUT_FORMAT", "markdown")  # markdown, plain, json
    
    @classmethod
    def to_dict(cls) -> Dict:
        """Convert settings to dictionary."""
        return {
            "max_prompt_length": cls.MAX_PROMPT_LENGTH,
            "min_prompt_length": cls.MIN_PROMPT_LENGTH,
            "prefer_structured": cls.PREFER_STRUCTURED,
            "include_examples": cls.INCLUDE_EXAMPLES,
            "output_format": cls.OUTPUT_FORMAT,
        }


# Create settings instance
settings = Settings()

