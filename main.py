"""
Main entry point for the ChatGPT Prompt Optimization Agent.
"""

from agent.optimizer import PromptOptimizer
import sys


def main():
    """Main function to run the prompt optimizer."""
    if len(sys.argv) < 2:
        print("Usage: python main.py '<your natural language prompt>'")
        print("Example: python main.py 'Write me a story about a robot'")
        sys.exit(1)
    
    # Get input from command line
    natural_language_text = " ".join(sys.argv[1:])
    
    # Initialize optimizer
    optimizer = PromptOptimizer()
    
    # Optimize the prompt
    print("Processing natural language text...")
    optimized_prompt = optimizer.optimize(natural_language_text)
    
    # Display results
    print("\n" + "="*50)
    print("OPTIMIZED PROMPT:")
    print("="*50)
    print(optimized_prompt)
    print("="*50)


if __name__ == "__main__":
    main()

