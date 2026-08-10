---
title: "What is an AI agent and how does it differ from a standard LLM?"
id: 23
category: "AI Agents and MCP"
difficulty: "Beginner"
tags:
  - ai-engineering
  - ai-agents-and-mcp
  - interview-questions
---

# What is an AI agent and how does it differ from a standard LLM?

**Short answer:** A standard LLM is a stateless text-in, text-out model that generates completion tokens based on a static prompt; an AI agent is an autonomous system that uses an LLM as its central reasoning engine to execute multi-step plans, invoke external tools, maintain state, and evaluate environment feedback to achieve a goal.

## Detail

The transition from a raw LLM to an AI Agent introduces three key operational loops:

```text
                  ┌───────────────────────────┐
                  ▼                           │
[User Goal] ──► [LLM Planner] ──► [Tool Call] ──► [Environment Observation]
```

1. **Perception & Planning:** The LLM receives goals, formulates plans, and selects actions.
2. **Action & Tool Execution:** Executing API calls, database queries, shell scripts, or web browsing.
3. **Observation & Reflection:** Feeding execution outputs and errors back into the LLM context to determine next steps or retry failed operations.

| Core Dimension       | Standard LLM                   | AI Agent                                      |
| -------------------- | ------------------------------ | --------------------------------------------- |
| **Execution Style**  | Single forward-pass generation | Multi-turn reasoning loop                     |
| **Tool Integration** | None (pure text generation)    | External APIs, DBs, search engines, sandboxes |
| **State & Memory**   | Ephemeral context window       | Persistent memory (short-term & long-term)    |
| **Autonomy**         | Passive responder              | Active goal-directed executor                 |

## Example

Conceptual Python structure of an agent execution loop:

```python
class Agent:
    def __init__(self, llm, tools: dict):
        self.llm = llm
        self.tools = tools
        self.memory = []

    def run(self, goal: str, max_steps: int = 5):
        self.memory.append({"role": "user", "content": goal})

        for step in range(max_steps):
            response = self.llm.generate(self.memory)
            if response.is_final_answer:
                return response.answer

            # Execute tool action selected by LLM
            tool_result = self.tools[response.tool_name](**response.tool_args)
            self.memory.append({"role": "tool", "content": str(tool_result)})

        return "Max steps reached without completion."
```

## Interview tips

- Emphasize that agent loops require strict termination criteria (max step counts, timeout bounds, and budget limits) to avoid infinite execution loops.
- Highlight the role of structured function calling (JSON schema) in driving reliable agent tool invocation.

---

[⬅ Back to AI Agents and MCP](./README.md) · [All topics](../README.md)
