"""
Interactive prompt optimization tool.
Run this to interactively optimize prompts.
"""

from agent.optimizer import PromptOptimizer

def main():
    """Interactive prompt optimizer."""
    print("=" * 60)
    print("ChatGPT Prompt Optimization Agent - Interactive Mode")
    print("=" * 60)
    print("Enter your natural language prompts to get optimized versions.")
    print("Type 'quit', 'exit', or 'q' to stop.\n")
    
    optimizer = PromptOptimizer()
    
    while True:
        try:
            user_input = input("Enter your prompt: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye!")
                break
            
            print("\nProcessing...")
            optimized = optimizer.optimize(user_input)
            
            print("\n" + "="*60)
            print("OPTIMIZED PROMPT:")
            print("="*60)
            print(optimized)
            print("="*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")
            continue

if __name__ == "__main__":
    main()

