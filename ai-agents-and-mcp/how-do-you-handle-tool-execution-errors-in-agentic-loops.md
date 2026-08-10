---
title: "How do you handle tool execution errors in agentic loops?"
id: 68
category: "AI Agents and MCP"
difficulty: "Beginner"
tags:
  - ai-engineering
  - ai-agents-and-mcp
  - interview-questions
---

# How do you handle tool execution errors in agentic loops?

**Short answer:** Tool execution errors in agentic loops are handled by capturing runtime exceptions (timeouts, invalid JSON arguments, 4xx/5xx HTTP codes), formatting them into structured `role: "tool"` error messages, and appending them to the conversation context so the LLM can self-correct its next tool invocation.

## Detail

If an external tool call fails (e.g. invalid SQL syntax or broken API key), crashing the python process breaks the agent loop.

```text
[Tool Invocation Failed] ──► Catch Exception ──► Format Error String ──► Append to Agent Context
                                                                                 │
[LLM Evaluates Error]   ◄── Re-evaluate Parameters ◄── "SQL syntax error at line 1" ┘
```

### Self-Correction Strategy

1. **Graceful Exception Capture:** Wrap tool execution in `try-except` blocks.
2. **Descriptive Error Payloads:** Return explicit error details (e.g. `"Tool Error: Missing required parameter 'database_name'"`) rather than vague generic failures (`"Error 500"`).
3. **Retry Counter:** Limit consecutive tool failure retries (e.g. max 3 retries per tool) to prevent infinite loops.

## Example

Python agentic exception handler pattern:

```python
def safe_tool_executor(tool_fn, tool_args: dict) -> str:
    try:
        result = tool_fn(**tool_args)
        return f"Tool Success: {result}"
    except TypeError as e:
        return f"Tool Parameter Error: Invalid arguments provided. Details: {e}. Please correct parameter keys."
    except Exception as e:
        return f"Tool Runtime Failure: {e}. Consider trying an alternative tool or approach."
```

## Interview tips

- Emphasize that descriptive error messages allow models to learn from runtime mistakes within the same conversation loop.
- Discuss setting max step bounds to terminate failing agent tasks cleanly.

---

[⬅ Back to AI Agents and MCP](./README.md) · [All topics](../README.md)
