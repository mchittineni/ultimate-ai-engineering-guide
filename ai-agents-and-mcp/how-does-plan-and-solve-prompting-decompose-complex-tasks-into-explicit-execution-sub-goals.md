---
title: "How does Plan-and-Solve prompting decompose complex tasks into explicit execution sub-goals?"
id: 136
category: "AI Agents and MCP"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - ai-agents-and-mcp
  - interview-questions
---

# How does Plan-and-Solve prompting decompose complex tasks into explicit execution sub-goals?

**Short answer:** Plan-and-Solve prompting decouples planning from execution: an initial LLM pass explicitly generates a high-level step-by-step plan (sub-goals) before executing individual steps sequentially or in parallel, preventing greedy reasoning mistakes inherent in pure ReAct loops.

## Detail

Standard ReAct loops operate greedily token-by-token: the agent decides its next action without a holistic view of the overall task workflow.

```
ReAct (Greedy Step-by-Step):  Step 1 Action ──► Step 2 Action ──► Re-eval (Risk of deadlocks)

Plan-and-Solve (Two-Phase):
Phase 1: [Planner LLM] ──► Generate Plan: [Step 1: Scrape, Step 2: Extract, Step 3: Summarize]
Phase 2: [Executor LLM] ──► Execute Step 1 ──► Execute Step 2 ──► Execute Step 3
```

### Key Framework Advantages

1. **Global Optimization:** The planner outlines dependencies (e.g. *"Step 3 requires output from Step 1 and Step 2"*) prior to spending API tokens on tool calls.
2. **Dynamic Replanning:** If Step 2 tool execution returns an unexpected error, a replanner module adjusts remaining sub-goals.

## Example

Python concept for Plan-and-Solve task execution:

```python
def plan_and_solve_pipeline(user_goal: str, planner_fn, executor_fn):
    # Phase 1: Generate explicit execution plan
    plan_prompt = f"Decompose this goal into numbered sub-goals: '{user_goal}'"
    plan_steps = planner_fn(plan_prompt) # e.g. ["1. Fetch data", "2. Calculate totals", "3. Format markdown"]
    
    # Phase 2: Execute plan sub-goals sequentially
    execution_context = {}
    for step in plan_steps:
        result = executor_fn(step, execution_context)
        execution_context[step] = result
        
    return execution_context
```

## Interview tips

- Contrast Plan-and-Solve with ReAct: Plan-and-Solve excels at structured multi-step batch tasks, while ReAct excels at open-ended exploratory investigation.
- Connect Plan-and-Solve to LangChain / AutoGen Plan-and-Execute agent architectures.

## Related Concepts

- [[How does Graph-of-Thoughts (GoT) extend Tree-of-Thoughts for arbitrary network reasoning?]] (`#119`): [How does Graph-of-Thoughts (GoT) extend Tree-of-Thoughts for arbitrary network reasoning?](../prompt-engineering/how-does-graph-of-thoughts-got-extend-tree-of-thoughts-for-arbitrary-network-reasoning.md)
- [[How do DAG-based Multi-Agent Orchestrators prevent state deadlocks?]] (`#139`): [How do DAG-based Multi-Agent Orchestrators prevent state deadlocks?](../ai-agents-and-mcp/how-do-dag-based-multi-agent-orchestrators-prevent-state-deadlocks.md)
- [[How to design an autonomous multi-agent software engineering system in a staff-level interview?]] (`#200`): [How to design an autonomous multi-agent software engineering system in a staff-level interview?](../interview-experience/how-to-design-an-autonomous-multi-agent-software-engineering-system-in-a-staff-level-interview.md)

---

[⬅ Back to AI Agents and MCP](./README.md) · [All topics](../README.md)
