"""
Main prompt optimizer module that coordinates the optimization process.
"""

from agent.parser import NaturalLanguageParser
from agent.validator import PromptValidator
from typing import Dict, Optional, List
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
        Build an optimized prompt from parsed data following OpenAI's reasoning best practices.
        
        Based on: https://platform.openai.com/docs/guides/reasoning-best-practices
        
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
        original_text = parsed_data.get("original_text", "")
        
        # Determine if this is a complex task (requires step-by-step)
        is_complex = self._is_complex_task(intent, requirements)
        
        # Determine appropriate role based on intent
        role = self._determine_role(intent)
        
        # Build structured prompt using OpenAI best practices
        prompt_parts = []
        
        # 1. Role assignment (OpenAI best practice: assign specific roles)
        if role:
            prompt_parts.append(f"You are {role}.")
        
        # 2. Main instruction with delimiters (OpenAI best practice: use delimiters)
        # Clear and specific instructions
        main_instruction = self._create_main_instruction(intent, original_text)
        prompt_parts.append(main_instruction)
        
        # 3. Context with delimiters (OpenAI best practice: provide reference text)
        if context:
            prompt_parts.append(f"\nContext:\n\"\"\"{context}\"\"\"")
        
        # 4. Requirements as constraints
        if requirements:
            prompt_parts.append("\nRequirements:")
            for req in requirements:
                prompt_parts.append(f"- {req}")
        
        # 5. Chain-of-thought for complex tasks (OpenAI best practice)
        if is_complex:
            steps = self._generate_steps(intent, requirements)
            if steps:
                prompt_parts.append("\nPlease follow these steps:")
                for i, step in enumerate(steps, 1):
                    prompt_parts.append(f"{i}. {step}")
        
        # 6. Output format specification (OpenAI best practice: specify desired format)
        format_spec = self._create_output_format_spec(output_format, intent)
        if format_spec:
            prompt_parts.append(f"\n{format_spec}")
        
        # 7. Additional best practices
        prompt_parts.append("\nPlease be specific, clear, and comprehensive in your response.")
        
        # Combine into final prompt
        optimized_prompt = "\n".join(prompt_parts)
        
        return optimized_prompt
    
    def _is_complex_task(self, intent: str, requirements: List[str]) -> bool:
        """Determine if task requires step-by-step approach."""
        complex_indicators = [
            "analyze", "create", "build", "develop", "design", "write",
            "report", "plan", "explain", "compare", "evaluate"
        ]
        
        intent_lower = intent.lower()
        has_complex_indicator = any(indicator in intent_lower for indicator in complex_indicators)
        has_multiple_requirements = len(requirements) >= 2
        
        return has_complex_indicator or has_multiple_requirements
    
    def _determine_role(self, intent: str) -> str:
        """Determine appropriate role based on intent."""
        intent_lower = intent.lower()
        
        role_mappings = {
            "story": "an expert creative writer",
            "write": "an expert writer",
            "explain": "an expert educator",
            "analyze": "an expert data analyst",
            "code": "an expert software developer",
            "design": "an expert designer",
            "plan": "an expert strategist",
            "report": "an expert analyst",
            "create": "a creative professional",
        }
        
        for keyword, role in role_mappings.items():
            if keyword in intent_lower:
                return role
        
        return "an expert assistant"
    
    def _create_main_instruction(self, intent: str, original_text: str) -> str:
        """Create clear and specific main instruction."""
        # Use delimiters to separate instruction from input (OpenAI best practice)
        if original_text and len(original_text) > len(intent) + 10:
            # Use the original text as input with delimiters
            # For clarity, extract just the core task
            core_task = intent if len(intent) < 50 else intent[:50] + "..."
            return f"Please complete the following task:\n\n\"\"\"{original_text}\"\"\""
        else:
            # If original text is not much longer, just use intent
            return f"Task: {intent}."
    
    def _generate_steps(self, intent: str, requirements: List[str]) -> List[str]:
        """Generate step-by-step instructions for complex tasks."""
        steps = []
        intent_lower = intent.lower()
        
        # Generic steps for different task types
        if "write" in intent_lower or "story" in intent_lower:
            steps = [
                "Plan the structure and key elements",
                "Develop the content with clear narrative",
                "Review and refine for clarity and engagement"
            ]
        elif "analyze" in intent_lower or "report" in intent_lower:
            steps = [
                "Identify key data points and information",
                "Analyze patterns and relationships",
                "Present findings in a clear, structured format"
            ]
        elif "explain" in intent_lower:
            steps = [
                "Break down the concept into understandable parts",
                "Provide examples and analogies",
                "Summarize key takeaways"
            ]
        elif "create" in intent_lower or "build" in intent_lower:
            steps = [
                "Define the requirements and scope",
                "Design the approach or structure",
                "Implement the solution step by step"
            ]
        else:
            # Generic steps
            steps = [
                "Understand the requirements",
                "Break down into manageable components",
                "Execute systematically"
            ]
        
        return steps
    
    def _create_output_format_spec(self, output_format: str, intent: str) -> str:
        """Create detailed output format specification."""
        if output_format:
            return f"Output Format: Provide your response in {output_format} format."
        
        # Infer format from intent
        intent_lower = intent.lower()
        format_hints = {
            "story": "narrative format with clear paragraphs",
            "report": "structured format with sections and headings",
            "list": "bulleted or numbered list format",
            "code": "code format with syntax highlighting",
            "explain": "clear explanation with examples",
            "analyze": "analysis format with findings and conclusions"
        }
        
        for keyword, format_desc in format_hints.items():
            if keyword in intent_lower:
                return f"Output Format: Provide your response in {format_desc}."
        
        return ""

