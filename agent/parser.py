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
                
                # Remove pronouns and unnecessary words at the start
                # Remove "me", "us", "you" if they appear right after the action verb
                intent = re.sub(r'^(me|us|you|for\s+me|for\s+us)\s+', '', intent, flags=re.IGNORECASE)
                
                # Clean up articles
                intent = re.sub(r'^(a|an|the)\s+', '', intent, flags=re.IGNORECASE)
                
                # If intent is too short or just "me", try to get more context
                if len(intent.split()) <= 2 and "me" in intent.lower():
                    # Try alternative patterns
                    alt_patterns = [
                        r"(?:write|create|generate|make|build|develop)\s+(?:me\s+)?(?:a\s+)?(.+?)(?:\.|$)",
                        r"(?:write|create|generate|make|build|develop)\s+(.+?)(?:\.|$)",
                    ]
                    for alt_pattern in alt_patterns:
                        alt_match = re.search(alt_pattern, text_lower, re.IGNORECASE)
                        if alt_match:
                            intent = alt_match.group(1).strip()
                            intent = re.sub(r'^(me|us|you|for\s+me|for\s+us|a|an|the)\s+', '', intent, flags=re.IGNORECASE)
                            break
                
                return intent.strip()
        
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
        # Look for context indicators - improved patterns
        context_patterns = [
            r"given\s+(?:that\s+)?(.+?)(?:,|\.|\s+explain|\s+write|\s+create)",
            r"assuming\s+(?:that\s+)?(.+?)(?:,|\.|\s+explain|\s+write|\s+create)",
            r"for\s+(?:a\s+)?(.+?)(?:,|\.|\s+write|\s+create|\s+explain)",
            r"(?:context|background|situation):\s*(.+?)(?:\.|$)",
            r"as\s+(?:a\s+)?(.+?)(?:,|\.|\s+explain|\s+write)",
        ]
        
        for pattern in context_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                context = match.group(1).strip()
                # Clean up common prefixes
                context = re.sub(r'^(a|an|the)\s+', '', context, flags=re.IGNORECASE)
                if len(context) > 3:  # Only return if meaningful
                    return context
        
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
        text_lower = text.lower()
        
        # Direct format mentions (json, markdown, etc.)
        direct_formats = ["json", "xml", "markdown", "html", "csv", "yaml"]
        for fmt in direct_formats:
            if fmt in text_lower:
                # Check if it's about output format, not just mentioned
                format_pattern = rf"(?:in|as|with|using)\s+(?:a|an)?\s*{fmt}"
                if re.search(format_pattern, text_lower):
                    return fmt
        
        # Format type patterns
        format_patterns = [
            r"(?:in|as|with|using)\s+(?:a|an)?\s*(?:output\s+)?(?:format|structure|style|type|form)\s+(?:of\s+)?(.+?)(?:\.|$)",
            r"(?:format|structure|style)\s*:\s*(.+?)(?:\.|$)",
        ]
        
        for pattern in format_patterns:
            match = re.search(pattern, text_lower)
            if match:
                format_desc = match.group(1).strip()
                # Remove "format" if it's just "format format"
                if format_desc.lower() == "format":
                    continue
                return format_desc
        
        return ""

