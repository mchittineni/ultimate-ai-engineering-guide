---
title: "How does LLM tool use and function calling work?"
id: 24
category: "AI Agents and MCP"
difficulty: "Beginner"
tags:
  - ai-engineering
  - ai-agents-and-mcp
  - interview-questions
---

# How does LLM tool use and function calling work?

**Short answer:** Function calling enables an LLM to inspect available tool definitions (JSON schemas passed in the system prompt), decide when a user request requires external capabilities, and output a structured JSON payload containing the function name and arguments instead of prose text.

## Detail

LLMs cannot execute code or access external systems directly. Function calling establishes a structured protocol between the model and an execution environment:

1. **Registration:** Client provides available tool signatures defined via JSON Schema (function name, description, parameter types, required fields).
2. **Model Selection:** The model evaluates whether the user intent matches a registered tool. If matched, it sets `finish_reason="tool_calls"` and returns JSON arguments.
3. **Client Execution:** The client system parses the JSON, executes the actual code/API call locally or in a sandbox, and retrieves the output string.
4. **Final Response Generation:** Client sends the execution result back to the model as a `tool` role message so the model can summarize or continue reasoning.

## Example

Example OpenAI Python SDK function calling pattern:

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Fetch real-time stock ticker price",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Stock symbol, e.g. NVDA"}
                },
                "required": ["ticker"]
            }
        }
    }
]

# LLM output payload when tool is invoked:
tool_call_payload = {
    "name": "get_stock_price",
    "arguments": '{"ticker": "NVDA"}'
}
```

## Interview tips

- Note that fine-tuned models (e.g. Claude, GPT-4, Llama 3) have specialized tool-calling tokens to distinguish tool requests from standard text responses.
- Emphasize validating tool argument JSON schemas (e.g., using Pydantic) prior to executing any tool code.

---

[⬅ Back to AI Agents and MCP](./README.md) · [All topics](../README.md)
