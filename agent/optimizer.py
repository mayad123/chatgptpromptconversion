"""
Main prompt optimizer module that coordinates the optimization process.
"""

from agent.parser import NaturalLanguageParser
from agent.validator import PromptValidator
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PromptOptimizer:
    """
    Main class for optimizing natural language text into ChatGPT prompts.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the prompt optimizer.
        
        Args:
            config: Optional configuration dictionary
        """
        self.parser = NaturalLanguageParser()
        self.validator = PromptValidator()
        self.config = config or {}
        
    def optimize(self, natural_language_text: str) -> str:
        """
        Convert natural language text to an optimized ChatGPT prompt.
        
        Args:
            natural_language_text: The natural language input to optimize
            
        Returns:
            Optimized prompt string
        """
        logger.info("Starting prompt optimization...")
        
        # Parse natural language to extract intent and requirements
        parsed_data = self.parser.parse(natural_language_text)
        logger.info(f"Parsed intent: {parsed_data.get('intent')}")
        
        # Build optimized prompt structure
        optimized_prompt = self._build_prompt(parsed_data)
        
        # Validate the optimized prompt
        validation_result = self.validator.validate(optimized_prompt)
        
        if not validation_result["is_valid"]:
            logger.warning(f"Validation issues: {validation_result['issues']}")
            # Apply fixes or warnings
        
        return optimized_prompt
    
    def _build_prompt(self, parsed_data: Dict) -> str:
        """
        Build an optimized prompt from parsed data.
        
        Args:
            parsed_data: Parsed natural language data
            
        Returns:
            Optimized prompt string
        """
        # Extract components
        intent = parsed_data.get("intent", "")
        context = parsed_data.get("context", "")
        requirements = parsed_data.get("requirements", [])
        output_format = parsed_data.get("output_format", "")
        
        # Build structured prompt using best practices
        prompt_parts = []
        
        # Add context if available
        if context:
            prompt_parts.append(f"Context: {context}")
        
        # Add main instruction
        prompt_parts.append(f"Task: {intent}")
        
        # Add requirements if any
        if requirements:
            prompt_parts.append("\nRequirements:")
            for req in requirements:
                prompt_parts.append(f"- {req}")
        
        # Add output format if specified
        if output_format:
            prompt_parts.append(f"\nOutput Format: {output_format}")
        
        # Combine into final prompt
        optimized_prompt = "\n".join(prompt_parts)
        
        return optimized_prompt

