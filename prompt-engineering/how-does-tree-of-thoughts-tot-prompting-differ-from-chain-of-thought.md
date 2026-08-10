---
title: "How does Tree-of-Thoughts (ToT) prompting differ from Chain-of-Thought?"
id: 18
category: "Prompt Engineering"
difficulty: "Advanced"
tags:
  - ai-engineering
  - prompt-engineering
  - interview-questions
---

# How does Tree-of-Thoughts (ToT) prompting differ from Chain-of-Thought?

**Short answer:** While Chain-of-Thought (CoT) generates a single linear path of reasoning steps, Tree-of-Thoughts (ToT) maintains a tree structure of multiple candidate reasoning steps, evaluating intermediate thoughts and exploring branches using search algorithms like Breadth-First Search (BFS) or Depth-First Search (DFS) with backtracking.

## Detail

For complex decision-making, creative writing, or mathematical puzzles (e.g., Game of 24), linear CoT often makes an early incorrect choice and cannot backtrack.

### Mechanics of Tree-of-Thoughts (ToT)

1. **Thought Decomposition:** The problem is broken down into discrete intermediate thought steps.
2. **Thought Generation:** At each state, the LLM generates $k$ prospective next thoughts (branching).
3. **State Evaluation:** The LLM evaluates each candidate state (e.g., scoring viability as `Sure`, `Maybe`, `Impossible`).
4. **Search Algorithm:** BFS or DFS navigates the search tree, pruning dead ends and backtracking when a path fails evaluation.

| Strategy                   | Search Space                             | Backtracking Capability                | Computational Cost                      |
| -------------------------- | ---------------------------------------- | -------------------------------------- | --------------------------------------- |
| **Chain-of-Thought (CoT)** | Single linear path ($1 \times N$)        | None                                   | Low (1 LLM call, $O(N)$ tokens)         |
| **Tree-of-Thoughts (ToT)** | Branching tree, $k^d$ paths at depth $d$ | Full backtracking via state evaluation | High ($O(b \cdot k \cdot d)$ LLM calls) |

The unpruned tree grows as $k^d$, but you never expand all of it: keeping a beam of $b$ states per level and generating $k$ candidates from each costs $O(b \cdot k \cdot d)$ generation calls plus the same order of evaluation calls. That bounded beam is what makes ToT affordable — and it is the number to quote when an interviewer asks what ToT costs.

## Example

Conceptual Python algorithm for BFS Tree-of-Thoughts search:

```python
def tree_of_thoughts_bfs(initial_state, generate_thoughts_fn, evaluate_state_fn, max_depth=3):
    current_states = [initial_state]

    for depth in range(max_depth):
        next_candidates = []
        for state in current_states:
            # Step 1: Generate k prospective next thoughts
            thoughts = generate_thoughts_fn(state, num_samples=3)
            for thought in thoughts:
                new_state = f"{state} -> {thought}"
                # Step 2: Evaluate state score
                score = evaluate_state_fn(new_state)
                if score > 0.5: # Prune unviable branches
                    next_candidates.append((new_state, score))

        # Select top-k viable states for next depth step
        next_candidates.sort(key=lambda x: x[1], reverse=True)
        current_states = [state for state, _ in next_candidates[:2]]

    return current_states[0] if current_states else None
```

## Interview tips

- Highlight that ToT trades off latency and token budget for significantly higher solving accuracy on complex planning problems.
- Note how modern agent frameworks (like Monte Carlo Tree Search in reasoning models) build upon ToT search concepts natively.

---

[⬅ Back to Prompt Engineering](./README.md) · [All topics](../README.md)
