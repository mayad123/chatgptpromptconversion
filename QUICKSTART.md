# Quick Start Guide

## Option 1: Run Without Installing Dependencies (Recommended to Start)

The core agent works with Python's standard library only! You can run it immediately:

```bash
python main.py "Write me a story about a robot"
```

## Option 2: Install Optional Dependencies

If you want enhanced features (like .env file support, token counting), install optional dependencies:

```bash
pip install -r requirements.txt
```

Or install just what you need:
```bash
pip install python-dotenv  # For .env file support
pip install tiktoken       # For accurate token counting
```

## Usage Examples

### 1. Command Line Usage

```bash
# Basic usage
python main.py "Write a blog post about AI"

# With context
python main.py "Given that I'm a beginner, explain machine learning"

# Complex prompt
python main.py "Create a data analysis report that should include charts and must be in markdown format"
```

### 2. Python Script Usage

Create a file `my_script.py`:

```python
from agent.optimizer import PromptOptimizer

optimizer = PromptOptimizer()
result = optimizer.optimize("Write me a story about time travel")
print(result)
```

Run it:
```bash
python my_script.py
```

### 3. Interactive Usage

Create a file `interactive.py`:

```python
from agent.optimizer import PromptOptimizer

optimizer = PromptOptimizer()

while True:
    user_input = input("\nEnter your prompt (or 'quit' to exit): ")
    if user_input.lower() in ['quit', 'exit', 'q']:
        break
    
    optimized = optimizer.optimize(user_input)
    print("\n" + "="*50)
    print("OPTIMIZED PROMPT:")
    print("="*50)
    print(optimized)
    print("="*50)
```

Run it:
```bash
python interactive.py
```

## Test the Installation

Try the example file:

```bash
python examples/example_usage.py
```

## Troubleshooting

**Issue**: "No module named 'agent'"
- **Solution**: Make sure you're in the project root directory (`ChatGPTPromptOptimization`)

**Issue**: Import errors with dotenv or tiktoken
- **Solution**: These are optional. The agent works without them. Or install them: `pip install python-dotenv tiktoken`

## Next Steps

- Check out `examples/example_usage.py` for more examples
- Modify `agent/parser.py` to improve natural language parsing
- Enhance `agent/validator.py` with more validation rules
- Add your own custom prompt templates in `agent/optimizer.py`

