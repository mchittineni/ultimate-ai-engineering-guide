---
title: "What is an agent system prompt and how does it define tool availability?"
id: 135
category: "AI Agents and MCP"
difficulty: "Beginner"
tags:
  - ai-engineering
  - ai-agents-and-mcp
  - interview-questions
---

# What is an agent system prompt and how does it define tool availability?

**Short answer:** An agent system prompt defines the operational persona, goal-directed reasoning guidelines, safety constraints, and available tool descriptions, instructing the LLM when and how to generate valid function calls to achieve complex tasks.

## Detail

Without a structured system prompt, an LLM treats tool schemas as passive JSON definitions rather than active executable capabilities.

```
[Agent System Prompt]
- Role: SQL Database Operations Specialist
- Goal: Answer user business queries by executing read-only SQL queries.
- Available Tools: [query_postgres_db, get_table_schema]
- Behavioral Rules: Always inspect schema before writing SQL. Never run DELETE/UPDATE.
```

### Core Architecture Components

1. **Role Directive:** Establishing domain authority and operational boundaries.
2. **Tool Awareness Section:** Dynamically injecting descriptions and JSON schemas of active tools.
3. **Execution Instructions:** Defining the ReAct loop cycle (Thought $\to$ Action $\to$ Observation $\to$ Final Answer).

## Example

Python dynamic agent system prompt generator:

```python
def generate_agent_system_prompt(role: str, tools: list[dict]) -> str:
    tool_descriptions = "\n".join(f"- `{t['name']}`: {t['description']}" for t in tools)
    prompt = f"""You are an autonomous AI Agent operating under the role: {role}.

AVAILABLE TOOLS:
{tool_descriptions}

OPERATIONAL RULES:
1. Always analyze the query step-by-step before selecting a tool.
2. If a tool invocation returns an error, modify parameters and retry.
3. Once all required information is gathered, output the final answer to the user."""
    return prompt

tools = [
    {"name": "search_docs", "description": "Searches internal technical documentation."},
    {"name": "execute_code", "description": "Runs sandboxed Python code scripts."}
]
print(generate_agent_system_prompt("Senior DevOps Engineer", tools))
```

## Interview tips

- Discuss dynamic tool injection: injecting only relevant tools based on user permissions or task intent to keep context windows compact.
- Connect system prompt design to preventing tool hallucinations.

## Related Concepts

- [[What is an agent tool schema and how do parameters get validated before invocation?]] (`#131`): [What is an agent tool schema and how do parameters get validated before invocation?](../ai-agents-and-mcp/what-is-an-agent-tool-schema-and-how-do-parameters-get-validated-before-invocation.md)
- [[What is semantic versioning for prompts and model configurations in production deployments?]] (`#164`): [What is semantic versioning for prompts and model configurations in production deployments?](../llmops-and-production-ai/what-is-semantic-versioning-for-prompts-and-model-configurations-in-production-deployments.md)
- [[How to prepare for an AI Engineer coding interview (raw SDK vs frameworks)?]] (`#191`): [How to prepare for an AI Engineer coding interview (raw SDK vs frameworks)?](../interview-experience/how-to-prepare-for-an-ai-engineer-coding-interview-raw-sdk-vs-frameworks.md)

---

[⬅ Back to AI Agents and MCP](./README.md) · [All topics](../README.md)
