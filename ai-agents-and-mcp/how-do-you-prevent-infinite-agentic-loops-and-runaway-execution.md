---
title: "How do you prevent infinite agentic loops and runaway execution?"
id: 70
category: "AI Agents and MCP"
difficulty: "Advanced"
tags:
  - ai-engineering
  - ai-agents-and-mcp
  - interview-questions
---

# How do you prevent infinite agentic loops and runaway execution?

**Short answer:** Infinite agent loops are prevented by enforcing hard step counters, maximum token and execution time budgets, cyclic state detection (hashing past tool call history), human-in-the-loop approval thresholds, and deterministic state graph bounds (e.g. LangGraph recursion limits).

## Detail

Autonomous agents operating in ReAct loops can get stuck repeatedly executing identical failing tool calls or oscillating between two unviable actions.

```text
[Agent Execution Loop]
         │
         ├── Step Counter >= Max Steps (e.g. 10) ──► TERMINATE (Step Limit)
         │
         ├── Cumulative Token Spend >= Budget     ──► TERMINATE (Budget Exceeded)
         │
         └── Tool History Hash Duplicate Detected  ──► TERMINATE (Cyclic Loop)
```

### Key Circuit Breakers

1. **Max Recursion Depth:** Set hard limits (e.g. `recursion_limit = 15`) in framework graph executors.
2. **Action Hash Loop Detection:** Maintain a hash set of `(tool_name, tool_args)` tuples executed in the current session. If the exact same call repeats 3 times consecutively with no state change, abort.
3. **Financial / Token Caps:** Track aggregate API token spend during the run; kill the process if spend exceeds $0.50.

## Example

Python loop detector snippet:

```python
import hashlib

class AgentCircuitBreaker:
    def __init__(self, max_steps=10, max_repeats=2):
        self.max_steps = max_steps
        self.max_repeats = max_repeats
        self.call_counts = {}
        self.current_step = 0

    def check_step(self, tool_name: str, tool_args: dict):
        self.current_step += 1
        if self.current_step > self.max_steps:
            raise RuntimeError("Circuit Breaker: Max execution steps reached.")

        # Create deterministic hash of tool call
        call_sig = f"{tool_name}:{str(sorted(tool_args.items()))}"
        call_hash = hashlib.md5(call_sig.encode()).hexdigest()

        self.call_counts[call_hash] = self.call_counts.get(call_hash, 0) + 1
        if self.call_counts[call_hash] > self.max_repeats:
            raise RuntimeError(f"Circuit Breaker: Cyclic loop detected on tool '{tool_name}'. Aborting.")
```

## Interview tips

- Emphasize that production AI agents must fail gracefully, returning structured status diagnostic reports to the user.
- Discuss human-in-the-loop (HITL) checkpoints before executing destructive actions (e.g. database deletes or external emails).

---

[⬅ Back to AI Agents and MCP](./README.md) · [All topics](../README.md)
