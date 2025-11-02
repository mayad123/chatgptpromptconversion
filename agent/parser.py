"""
Natural language parser for extracting intent and requirements from text.
"""

import re
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NaturalLanguageParser:
    """
    Parser for extracting structured information from natural language text.
    """
    
    def __init__(self):
        """Initialize the parser."""
        self.intent_patterns = [
            r"(?:write|create|generate|make|build|develop)\s+(.+?)(?:\.|$)",
            r"(?:explain|describe|tell me about)\s+(.+?)(?:\.|$)",
            r"(?:help|assist|guide)\s+(?:me\s+)?(?:with|to)\s+(.+?)(?:\.|$)",
            r"(?:i\s+)?(?:want|need|would like)\s+(?:to\s+)?(.+?)(?:\.|$)",
        ]
        
        self.requirement_keywords = [
            "should", "must", "need", "require", "include", 
            "with", "containing", "that", "having"
        ]
        
    def parse(self, text: str) -> Dict:
        """
        Parse natural language text to extract structured information.
        
        Args:
            text: Natural language input text
            
        Returns:
            Dictionary containing parsed data (intent, context, requirements, etc.)
        """
        text = text.strip()
        logger.info(f"Parsing text: {text[:50]}...")
        
        # Extract intent
        intent = self._extract_intent(text)
        
        # Extract context
        context = self._extract_context(text)
        
        # Extract requirements
        requirements = self._extract_requirements(text)
        
        # Extract output format hints
        output_format = self._extract_output_format(text)
        
        parsed_data = {
            "intent": intent,
            "context": context,
            "requirements": requirements,
            "output_format": output_format,
            "original_text": text
        }
        
        return parsed_data
    
    def _extract_intent(self, text: str) -> str:
        """
        Extract the main intent or goal from the text.
        
        Args:
            text: Input text
            
        Returns:
            Extracted intent string
        """
        text_lower = text.lower()
        
        # Try to match intent patterns
        for pattern in self.intent_patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                intent = match.group(1).strip()
                # Clean up the intent
                intent = re.sub(r'^(a|an|the)\s+', '', intent, flags=re.IGNORECASE)
                return intent
        
        # If no pattern matches, use the original text as intent
        return text
    
    def _extract_context(self, text: str) -> str:
        """
        Extract context or background information.
        
        Args:
            text: Input text
            
        Returns:
            Extracted context string
        """
        # Look for context indicators
        context_patterns = [
            r"(?:given|assuming|for|in)\s+(.+?)(?:,|\.|$)",
            r"(?:context|background|situation):\s*(.+?)(?:\.|$)",
        ]
        
        for pattern in context_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _extract_requirements(self, text: str) -> List[str]:
        """
        Extract specific requirements or constraints.
        
        Args:
            text: Input text
            
        Returns:
            List of requirement strings
        """
        requirements = []
        
        # Look for requirement patterns
        for keyword in self.requirement_keywords:
            pattern = rf"(?:it|the|this)\s+(?:should|must|need|require|include)\s+(.+?)(?:\.|,|$)"
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                req = match.group(1).strip()
                if req:
                    requirements.append(req)
        
        # Look for list-like requirements
        list_pattern = r"(?:should|must|need)\s+be\s+(.+?)(?:\.|$)"
        matches = re.finditer(list_pattern, text, re.IGNORECASE)
        for match in matches:
            req = match.group(1).strip()
            if req:
                requirements.append(req)
        
        return list(set(requirements))  # Remove duplicates
    
    def _extract_output_format(self, text: str) -> str:
        """
        Extract hints about desired output format.
        
        Args:
            text: Input text
            
        Returns:
            Output format string
        """
        format_keywords = [
            "format", "structure", "style", "type", "form",
            "json", "xml", "markdown", "html", "csv", "list", "table"
        ]
        
        text_lower = text.lower()
        for keyword in format_keywords:
            pattern = rf"(?:in|as|with|using)\s+(?:a|an)?\s*{keyword}\s+(?:of\s+)?(.+?)(?:\.|$)"
            match = re.search(pattern, text_lower)
            if match:
                return match.group(1).strip()
        
        return ""

