"""
Validator for checking prompt quality and best practices.
"""

from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PromptValidator:
    """
    Validates optimized prompts against best practices.
    """
    
    def __init__(self):
        """Initialize the validator."""
        self.min_length = 10
        self.max_length = 4000  # Typical ChatGPT token limit consideration
        self.required_elements = ["Task"]  # Minimum required elements
        
    def validate(self, prompt: str) -> Dict:
        """
        Validate a prompt against quality criteria.
        
        Args:
            prompt: The prompt to validate
            
        Returns:
            Dictionary with validation results (is_valid, issues, suggestions)
        """
        issues = []
        suggestions = []
        
        # Check length
        if len(prompt) < self.min_length:
            issues.append(f"Prompt is too short (minimum {self.min_length} characters)")
        
        if len(prompt) > self.max_length:
            issues.append(f"Prompt is too long (maximum {self.max_length} characters)")
            suggestions.append("Consider breaking into multiple prompts or summarizing")
        
        # Check for required elements
        for element in self.required_elements:
            if element.lower() not in prompt.lower():
                issues.append(f"Missing required element: {element}")
        
        # Check clarity (basic heuristic)
        if self._is_too_vague(prompt):
            suggestions.append("Consider adding more specific details or examples")
        
        # Check for best practices
        best_practice_checks = self._check_best_practices(prompt)
        suggestions.extend(best_practice_checks["suggestions"])
        
        is_valid = len(issues) == 0
        
        return {
            "is_valid": is_valid,
            "issues": issues,
            "suggestions": suggestions,
            "score": self._calculate_quality_score(prompt, issues)
        }
    
    def _is_too_vague(self, prompt: str) -> bool:
        """
        Check if prompt is too vague.
        
        Args:
            prompt: The prompt to check
            
        Returns:
            True if prompt seems vague
        """
        vague_indicators = [
            len(prompt.split()) < 10,  # Too few words
            prompt.count("?") > prompt.count("."),  # More questions than statements
        ]
        return any(vague_indicators)
    
    def _check_best_practices(self, prompt: str) -> Dict:
        """
        Check prompt against best practices.
        
        Args:
            prompt: The prompt to check
            
        Returns:
            Dictionary with suggestions
        """
        suggestions = []
        
        # Check for examples
        if "example" not in prompt.lower() and "sample" not in prompt.lower():
            suggestions.append("Consider adding examples for better clarity")
        
        # Check for role definition
        if "you are" not in prompt.lower() and "act as" not in prompt.lower():
            # This is optional, so just a suggestion
            pass
        
        # Check for step-by-step instructions for complex tasks
        word_count = len(prompt.split())
        if word_count > 100 and "step" not in prompt.lower():
            suggestions.append("For complex tasks, consider breaking into steps")
        
        return {"suggestions": suggestions}
    
    def _calculate_quality_score(self, prompt: str, issues: List[str]) -> float:
        """
        Calculate a quality score for the prompt (0-100).
        
        Args:
            prompt: The prompt
            issues: List of validation issues
            
        Returns:
            Quality score between 0 and 100
        """
        base_score = 100.0
        
        # Deduct for issues
        for issue in issues:
            if "too short" in issue.lower() or "too long" in issue.lower():
                base_score -= 20
            elif "missing" in issue.lower():
                base_score -= 15
            else:
                base_score -= 10
        
        # Bonus for length (sweet spot around 100-500 words)
        word_count = len(prompt.split())
        if 100 <= word_count <= 500:
            base_score += 5
        
        return max(0, min(100, base_score))

