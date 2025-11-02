"""
Helper utility functions.
"""

import re
from typing import List, Optional
try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False


def format_prompt(prompt: str, style: str = "markdown") -> str:
    """
    Format a prompt according to specified style.
    
    Args:
        prompt: The prompt to format
        style: Format style (markdown, plain, json)
        
    Returns:
        Formatted prompt string
    """
    if style == "plain":
        return prompt
    elif style == "markdown":
        # Add markdown formatting
        lines = prompt.split("\n")
        formatted_lines = []
        for line in lines:
            if line.startswith("Context:"):
                formatted_lines.append(f"## {line}")
            elif line.startswith("Task:"):
                formatted_lines.append(f"### {line}")
            elif line.startswith("- "):
                formatted_lines.append(line)
            else:
                formatted_lines.append(line)
        return "\n".join(formatted_lines)
    elif style == "json":
        # Convert to JSON structure (basic implementation)
        sections = {}
        current_section = None
        current_content = []
        
        for line in prompt.split("\n"):
            if ":" in line and not line.startswith("- "):
                if current_section:
                    sections[current_section] = "\n".join(current_content)
                current_section = line.split(":")[0].strip()
                current_content = [line.split(":", 1)[1].strip()]
            else:
                if line.strip():
                    current_content.append(line.strip())
        
        if current_section:
            sections[current_section] = "\n".join(current_content)
        
        import json
        return json.dumps(sections, indent=2)
    
    return prompt


def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """
    Count tokens in text (approximation if tiktoken not available).
    
    Args:
        text: Text to count tokens for
        model: Model name for token counting
        
    Returns:
        Estimated token count
    """
    if TIKTOKEN_AVAILABLE:
        try:
            encoding = tiktoken.encoding_for_model(model)
            return len(encoding.encode(text))
        except Exception:
            pass
    
    # Fallback: rough estimation (1 token ≈ 4 characters for English)
    return len(text) // 4


def extract_keywords(text: str, min_length: int = 3) -> List[str]:
    """
    Extract keywords from text.
    
    Args:
        text: Text to extract keywords from
        min_length: Minimum keyword length
        
    Returns:
        List of keywords
    """
    # Remove common stopwords (basic list)
    stopwords = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "as", "is", "was", "are", "were", "been",
        "be", "have", "has", "had", "do", "does", "did", "will", "would",
        "should", "could", "may", "might", "must", "can", "this", "that",
        "these", "those", "i", "you", "he", "she", "it", "we", "they"
    }
    
    # Extract words
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Filter stopwords and short words
    keywords = [
        word for word in words 
        if word not in stopwords and len(word) >= min_length
    ]
    
    # Return unique keywords
    return list(set(keywords))


def clean_text(text: str) -> str:
    """
    Clean and normalize text.
    
    Args:
        text: Text to clean
        
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text

