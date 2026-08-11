---
title: "What is an agent tool schema and how do parameters get validated before invocation?"
id: 131
category: "AI Agents and MCP"
difficulty: "Beginner"
tags:
  - ai-engineering
  - ai-agents-and-mcp
  - interview-questions
---

# What is an agent tool schema and how do parameters get validated before invocation?

**Short answer:** An agent tool schema is a formal JSON Schema contract defining a tool's function name, natural language description, and required parameter types; pre-invocation validation uses validation engines (like Pydantic) to type-check LLM-generated arguments before executing underlying Python code.

## Detail

LLMs generate tool calls as raw JSON strings. Without strict schema validation, invalid parameter types (e.g. string passed instead of int) cause runtime crashes.

```text
LLM Function Call ──► JSON Arguments ──► [Pydantic Validator] ──► Execute Tool Python Function
                                                 │
                                                 ▼ (If Validation Fails)
                                        Return Error to Agent
```

### Core Elements of Tool Schemas

1. **Description String:** Natural language explanation instructing the LLM _when_ and _why_ to choose the tool.
2. **Property Schema:** JSON Schema data types (`string`, `integer`, `boolean`, `array`, `enum`).
3. **Required List:** Array of mandatory parameter names.

## Example

Pydantic tool schema definition and validation in Python:

```python
from pydantic import BaseModel, Field, ValidationError

class SQLQueryToolSchema(BaseModel):
    query: str = Field(description="ANSI SQL SELECT query to execute")
    limit: int = Field(default=100, ge=1, le=1000, description="Max rows to return")

def validate_and_execute(raw_args: dict):
    try:
        validated_args = SQLQueryToolSchema(**raw_args)
        return f"Executing valid SQL query (limit {validated_args.limit}): {validated_args.query}"
    except ValidationError as e:
        return f"Tool Argument Error: {e}"

print(validate_and_execute({"query": "SELECT * FROM users", "limit": 50}))
```

## Interview tips

- Emphasize that clear, descriptive tool descriptions in schemas are critical for LLM function routing accuracy.
- Discuss handling validation errors gracefully by returning validation feedback to the LLM agent for self-correction.

## Related Concepts

- [[What is an agent system prompt and how does it define tool availability?]] (`#135`): [What is an agent system prompt and how does it define tool availability?](../ai-agents-and-mcp/what-is-an-agent-system-prompt-and-how-does-it-define-tool-availability.md)
- [[How do sandbox execution environments secure Code Interpreter tools?]] (`#140`): [How do sandbox execution environments secure Code Interpreter tools?](../ai-agents-and-mcp/how-do-sandbox-execution-environments-secure-code-interpreter-tools.md)
- [[How to audit and secure Model Context Protocol (MCP) servers against unauthorized tool invocation?]] (`#190`): [How to audit and secure Model Context Protocol (MCP) servers against unauthorized tool invocation?](../ai-safety-and-governance/how-to-audit-and-secure-model-context-protocol-mcp-servers-against-unauthorized-tool-invocation.md)

---

[⬅ Back to AI Agents and MCP](./README.md) · [All topics](../README.md)
