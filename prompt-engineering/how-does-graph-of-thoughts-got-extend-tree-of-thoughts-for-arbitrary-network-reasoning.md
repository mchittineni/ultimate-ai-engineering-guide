---
title: "How does Graph-of-Thoughts (GoT) extend Tree-of-Thoughts for arbitrary network reasoning?"
id: 119
category: "Prompt Engineering"
difficulty: "Advanced"
tags:
  - ai-engineering
  - prompt-engineering
  - interview-questions
---

# How does Graph-of-Thoughts (GoT) extend Tree-of-Thoughts for arbitrary network reasoning?

**Short answer:** Graph-of-Thoughts (GoT) extends Tree-of-Thoughts (ToT) by modeling intermediate LLM reasoning steps as arbitrary directed graphs (DAGs), allowing reasoning thoughts to be combined, aggregated, and looped across non-linear execution topologies.

## Detail

Standard reasoning structures are strictly linear (Chain-of-Thought) or strictly hierarchical branching (Tree-of-Thoughts).

```
Chain-of-Thought (CoT):  Thought 1 ──► Thought 2 ──► Thought 3

Tree-of-Thoughts (ToT):  Thought 1 ──┬──► Thought 2a ──► Thought 3a
                                    └──► Thought 2b ──► Thought 3b

Graph-of-Thoughts (GoT): Thought 1a ──┐
                                     ├──► Aggregate Thought 3 ──► Refine Loop
                         Thought 1b ──┘
```

### Advanced Operations Supported in GoT

1. **Aggregation Operations:** Merging insights from 3 parallel reasoning branches into a unified summary node.
2. **Looping Operations:** Returning a generated thought node back to an earlier validation node for iterative improvement.
3. **Graph Transformations:** Dynamically dynamically adding, pruning, or combining thought nodes based on scoring metrics.

## Example

Python conceptual node aggregation step in Graph-of-Thoughts:

```python
class ThoughtNode:
    def __init__(self, id: str, content: str, score: float = 0.0):
        self.id = id
        self.content = content
        self.score = score
        self.parents = []

def aggregate_thoughts(node_a: ThoughtNode, node_b: ThoughtNode) -> ThoughtNode:
    merged_content = f"Combined Insight:\n- {node_a.content}\n- {node_b.content}"
    merged_node = ThoughtNode(id="merged_3", content=merged_content, score=(node_a.score + node_b.score) / 2.0)
    merged_node.parents = [node_a.id, node_b.id]
    return merged_node
```

## Interview tips

- Emphasize latency vs accuracy trade-offs: GoT requires multiple LLM invocations and graph management logic, but achieves higher accuracy on complex sorting, document merging, and multi-hop tasks.
- Connect GoT principles to multi-agent DAG architectures (LangGraph).

## Related Concepts

- [[How does Plan-and-Solve prompting decompose complex tasks into explicit execution sub-goals?]] (`#136`): [How does Plan-and-Solve prompting decompose complex tasks into explicit execution sub-goals?](../ai-agents-and-mcp/how-does-plan-and-solve-prompting-decompose-complex-tasks-into-explicit-execution-sub-goals.md)
- [[How do DAG-based Multi-Agent Orchestrators prevent state deadlocks?]] (`#139`): [How do DAG-based Multi-Agent Orchestrators prevent state deadlocks?](../ai-agents-and-mcp/how-do-dag-based-multi-agent-orchestrators-prevent-state-deadlocks.md)
- [[How to design an autonomous multi-agent software engineering system in a staff-level interview?]] (`#200`): [How to design an autonomous multi-agent software engineering system in a staff-level interview?](../interview-experience/how-to-design-an-autonomous-multi-agent-software-engineering-system-in-a-staff-level-interview.md)

---

[⬅ Back to Prompt Engineering](./README.md) · [All topics](../README.md)
