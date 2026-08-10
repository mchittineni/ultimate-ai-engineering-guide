---
title: "How do multi-agent architectures and hierarchical delegation work?"
id: 26
category: "AI Agents and MCP"
difficulty: "Advanced"
tags:
  - ai-engineering
  - ai-agents-and-mcp
  - interview-questions
---

# How do multi-agent architectures and hierarchical delegation work?

**Short answer:** Multi-agent architectures divide complex enterprise tasks among specialized LLM agents (e.g., Planner, Coder, Reviewer), using hierarchical delegation (supervisor-worker models) or network collaboration protocols to pass state, execute sub-tasks in parallel, and cross-validate outputs.

## Detail

Single-agent systems degrade as prompt complexity and tool counts grow (tool choice overload). Multi-agent systems apply software modularity principles to AI workloads.

```
                  ┌──────────────────────┐
                  │   Supervisor Agent   │
                  └──────────┬───────────┘
                             │ Delegates & Aggregates
             ┌───────────────┼───────────────┐
             ▼               ▼               ▼
      ┌────────────┐   ┌────────────┐   ┌────────────┐
      │  Research  │   │  Coding    │   │  QA / Code │
      │   Agent    │   │   Agent    │   │  Reviewer  │
      └────────────┘   └────────────┘   └────────────┘
```

### Multi-Agent Communication Topologies

1. **Hierarchical (Supervisor-Worker):** A central coordinator agent breaks down a task, assigns sub-tasks to specialized domain worker agents, and reviews candidate solutions before synthesizing the final output.
2. **Sequential (Pipeline / Relay):** Output of Agent A feeds directly into the prompt context of Agent B (e.g., Spec Writer $\rightarrow$ Developer $\rightarrow$ QA).
3. **Joint Collaboration / Peer-to-Peer:** Agents debate solutions in a shared message bus or round-robin conversation (e.g., AutoGen, CrewAI, LangGraph).

### State Graphs & Determinism

Modern enterprise multi-agent frameworks (e.g., **LangGraph**) model agents as state nodes in a directed graph (DAG or cyclical graph), controlling edge state transitions deterministically rather than relying on unstructured LLM chatter.

## Example

State transition logic in Python multi-agent supervisor pattern:

```python
class MultiAgentState(dict):
    messages: list
    next_agent: str

def supervisor_router(state: MultiAgentState) -> str:
    last_msg = state["messages"][-1]["content"]
    if "CODE_COMPLETE" in last_msg:
        return "reviewer_agent"
    elif "REVIEW_APPROVED" in last_msg:
        return "END"
    else:
        return "coder_agent"

# State router decides next node execution dynamically
print("Next target node:", supervisor_router({"messages": [{"content": "CODE_COMPLETE: Created auth module"}]}))
```

## Interview tips

- Discuss why naive multi-agent chat loops lead to infinite agent-to-agent chatter, high latency, and exploding API costs if graph state and stopping conditions aren't enforced.
- Contrast LangGraph state graphs with CrewAI role-based task delegation.

---

[⬅ Back to AI Agents and MCP](./README.md) · [All topics](../README.md)
