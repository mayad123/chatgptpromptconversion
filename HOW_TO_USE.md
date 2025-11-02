# How to Use the ChatGPT Prompt Optimization Agent

## ✅ Quick Start (No Installation Required!)

The agent works immediately with Python's standard library. Just run:

```bash
python main.py "Write me a story about a robot"
```

That's it! No dependencies needed.

---

## 📋 Three Ways to Use It

### 1. **Command Line** (Simplest)

Open a terminal in the project folder and run:

```bash
# Simple prompt
python main.py "Write a blog post about AI"

# Prompt with context (use quotes for multi-word inputs)
python main.py "Given that I'm a beginner, explain machine learning"

# Complex prompt
python main.py "Create a report that should include charts and must be in markdown format"
```

**Example Output:**
```
==================================================
OPTIMIZED PROMPT:
==================================================
Context: that I'm a beginner in Python
Task: how to use loops
==================================================
```

---

### 2. **Interactive Mode** (Best for Testing Multiple Prompts)

Run the interactive script:

```bash
python run_interactive.py
```

Then type your prompts one by one. Type `quit` to exit.

**Example Session:**
```
Enter your prompt: Write a story about a robot

==================================================
OPTIMIZED PROMPT:
==================================================
Task: story about a robot
==================================================

Enter your prompt: quit
Goodbye!
```

---

### 3. **In Your Own Python Code**

Create your own Python script:

```python
from agent.optimizer import PromptOptimizer

# Initialize the optimizer
optimizer = PromptOptimizer()

# Optimize a prompt
optimized = optimizer.optimize("Write me a story about a robot")
print(optimized)
```

Save and run:
```bash
python your_script.py
```

---

## 🧪 Try the Examples

See how it works with different types of prompts:

```bash
python examples/example_usage.py
```

This will show 4 different examples of prompt optimization.

---

## 📝 What It Does

The agent:
1. **Parses** your natural language input
2. **Extracts** intent, context, and requirements
3. **Structures** it into an optimized ChatGPT prompt format
4. **Validates** the prompt against best practices

**Input:** "Write me a story about a robot"  
**Output:** 
```
Task: story about a robot
```

---

## ⚙️ Optional Enhancements

Want more features? Install optional dependencies:

```bash
pip install python-dotenv  # For .env file support
pip install tiktoken      # For accurate token counting
```

But these are completely optional - the core agent works without them!

---

## 🔧 Troubleshooting

**Problem:** "No module named 'agent'"  
**Solution:** Make sure you're in the project root folder (`ChatGPTPromptOptimization`)

**Problem:** Import errors with dotenv or tiktoken  
**Solution:** These are optional. The agent works fine without them. You can ignore the warnings or install them with `pip install python-dotenv tiktoken`

---

## 💡 Tips

1. **Use quotes** for multi-word prompts: `python main.py "your text here"`
2. **Be specific** - more context = better optimization
3. **Try interactive mode** - easier for testing: `python run_interactive.py`

---

## 🚀 Next Steps

- Check out `examples/example_usage.py` for more examples
- Modify `agent/parser.py` to improve natural language parsing
- Enhance `agent/validator.py` with custom validation rules
- Customize `agent/optimizer.py` for your specific use case

