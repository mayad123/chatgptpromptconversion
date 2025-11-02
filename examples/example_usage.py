"""
Example usage of the ChatGPT Prompt Optimization Agent.

Run this from the project root directory:
    python examples/example_usage.py
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import agent
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agent.optimizer import PromptOptimizer


def main():
    """Demonstrate various usage examples."""
    
    # Initialize the optimizer
    optimizer = PromptOptimizer()
    
    # Example 1: Simple prompt
    print("=" * 60)
    print("Example 1: Simple Prompt")
    print("=" * 60)
    text1 = "Write me a story about a robot"
    optimized1 = optimizer.optimize(text1)
    print(f"Input: {text1}")
    print(f"\nOptimized:\n{optimized1}\n")
    
    # Example 2: Prompt with context
    print("=" * 60)
    print("Example 2: Prompt with Context")
    print("=" * 60)
    text2 = "Given that I'm a beginner in Python, explain how to use loops"
    optimized2 = optimizer.optimize(text2)
    print(f"Input: {text2}")
    print(f"\nOptimized:\n{optimized2}\n")
    
    # Example 3: Complex prompt with requirements
    print("=" * 60)
    print("Example 3: Complex Prompt with Requirements")
    print("=" * 60)
    text3 = "Create a data analysis report that should include charts and must be in markdown format"
    optimized3 = optimizer.optimize(text3)
    print(f"Input: {text3}")
    print(f"\nOptimized:\n{optimized3}\n")
    
    # Example 4: Creative writing prompt
    print("=" * 60)
    print("Example 4: Creative Writing Prompt")
    print("=" * 60)
    text4 = "Write a short story about time travel that includes a plot twist"
    optimized4 = optimizer.optimize(text4)
    print(f"Input: {text4}")
    print(f"\nOptimized:\n{optimized4}\n")


if __name__ == "__main__":
    main()

