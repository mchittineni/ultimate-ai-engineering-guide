---
title: "What is the ReAct loop (Thought, Action, Observation)?"
id: 66
category: "AI Agents and MCP"
difficulty: "Beginner"
tags:
  - ai-engineering
  - ai-agents-and-mcp
  - interview-questions
---

# What is the ReAct loop (Thought, Action, Observation)?

**Short answer:** The ReAct (Reasoning and Acting) loop is an agentic framework where an LLM alternates between generating explicit reasoning thoughts, executing external tool actions, and inspecting environment observations until a goal is achieved.

## Detail

Standard LLMs struggle with multi-turn problem solving if forced to choose actions blindly without explicit intermediate reasoning.

```
[Goal] ──► Thought: "I need to check stock price for NVDA."
       ──► Action: `get_stock_price(ticker="NVDA")`
       ──► Observation: `{"price": 135.50}`
       ──► Thought: "I have the price. I can now answer the user."
       ──► Final Answer: "NVIDIA is currently trading at $135.50."
```

### The 3 Core Components

1. **Thought:** The LLM generates explicit internal reasoning about what to do next.
2. **Action:** The LLM specifies a structured tool call (function name and arguments).
3. **Observation:** The execution environment runs the tool and appends the result back into the prompt context.

## Example

Python implementation of a basic ReAct loop parser:

```python
import re

def parse_react_step(llm_output: str) -> tuple[str, str, str]:
    thought_match = re.search(r"Thought:\s*(.*?)(?=Action:|$)", llm_output, re.DOTALL)
    action_match = re.search(r"Action:\s*(.*?)(?=Action Input:|$)", llm_output, re.DOTALL)
    action_input_match = re.search(r"Action Input:\s*(.*)", llm_output, re.DOTALL)
    
    thought = thought_match.group(1).strip() if thought_match else ""
    action = action_match.group(1).strip() if action_match else ""
    action_input = action_input_match.group(1).strip() if action_input_match else ""
    
    return thought, action, action_input

sample_llm_step = """Thought: I should search for recent weather data.
Action: weather_search
Action Input: {"location": "San Francisco"}"""

print("Parsed ReAct Step:", parse_react_step(sample_llm_step))
```

## Interview tips

- Highlight how ReAct enables error recovery: if an Action returns an error Observation, the next Thought can analyze the error and attempt a different tool call.
- Contrast ReAct loops with zero-shot function calling.

---

[⬅ Back to AI Agents and MCP](./README.md) · [All topics](../README.md)
