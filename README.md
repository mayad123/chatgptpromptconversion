# ChatGPT Prompt Optimization Agent

An intelligent agent that converts natural language text into optimized prompt structures for ChatGPT.

## Features

- Natural language input processing
- Prompt structure optimization
- Best practice enforcement
- Context-aware prompt generation

## Installation

**Good News**: The core agent works with Python's standard library only! You can run it immediately without installing anything:

```bash
python main.py "Write me a story about a robot"
```

**Optional Dependencies** (for enhanced features):
```bash
pip install -r requirements.txt
```

## Quick Usage

### Command Line
```bash
# Basic usage
python main.py "Write a blog post about AI"

# With multiple words (use quotes)
python main.py "Given that I'm a beginner, explain machine learning"
```

### Interactive Mode
```bash
python run_interactive.py
```

### Python Code
```python
from agent import PromptOptimizer

optimizer = PromptOptimizer()
optimized_prompt = optimizer.optimize("Write me a story about a robot")
print(optimized_prompt)
```

## Project Structure

```
ChatGPTPromptOptimization/
├── agent/
│   ├── __init__.py
│   ├── optimizer.py
│   ├── parser.py
│   └── validator.py
├── config/
│   └── settings.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── test_optimizer.py
│   └── test_parser.py
├── examples/
│   └── example_usage.py
├── requirements.txt
└── main.py
```