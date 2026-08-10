---
title: "How does Skeleton-of-Thought (SoT) speed up generation via parallel decoding?"
id: 60
category: "Prompt Engineering"
difficulty: "Advanced"
tags:
  - ai-engineering
  - prompt-engineering
  - interview-questions
---

# How does Skeleton-of-Thought (SoT) speed up generation via parallel decoding?

**Short answer:** Skeleton-of-Thought (SoT) is a prompt-level acceleration technique that prompts an LLM to first output a high-level answer skeleton (bullet points), and then expands each bullet point independently in parallel API calls, reducing overall response latency by up to $2-3\times$.

## Detail

Autoregressive token decoding is strictly sequential. Generating a 1000-word detailed report sequentially can take 15–20 seconds.

### The SoT Two-Stage Workflow

```text
[User Request] ──► Stage 1: Skeleton Generation ──► [Bullet 1, Bullet 2, Bullet 3]
                                                             │
                  ┌──────────────────────────────────────────┼──────────────────────────────────────────┐
                  ▼                                          ▼                                          ▼
     Stage 2: Expand Bullet 1 (Parallel)        Stage 2: Expand Bullet 2 (Parallel)        Stage 2: Expand Bullet 3 (Parallel)
                  │                                          │                                          │
                  └──────────────────────────────────────────┼──────────────────────────────────────────┘
                                                             ▼
                                             [Reassembled Final Response]
```

1. **Stage 1 (Skeleton):** Prompt model to output concise outline headers (e.g. 5 bullet points).
2. **Stage 2 (Parallel Point Expanding):** Issue 5 parallel LLM API requests simultaneously, each expanding a specific bullet point while referencing the skeleton context.
3. **Reassembly:** Stitch expanded points back together in order.

## Example

Async Python implementation concept for Skeleton-of-Thought:

```python
import asyncio

async def expand_skeleton_point(skeleton: str, point: str) -> str:
    prompt = f"Given outline: {skeleton}\nExpand point '{point}' in detail."
    # Simulate async LLM call
    await asyncio.sleep(0.5)
    return f"Detailed content for {point}..."

async def skeleton_of_thought_pipeline(user_query: str):
    # Step 1: Get skeleton outline
    skeleton_points = ["Point 1: System Architecture", "Point 2: Security", "Point 3: Evals"]

    # Step 2: Parallel execution via asyncio.gather
    tasks = [expand_skeleton_point(str(skeleton_points), pt) for pt in skeleton_points]
    expanded_sections = await asyncio.gather(*tasks)

    return "\n\n".join(expanded_sections)
```

## Interview tips

- Highlight latency savings: SoT trades sequential time $O(N_1 + N_2 + \dots + N_k)$ for parallel time $O(\max(N_i))$, achieving dramatic speedups.
- Discuss limitations: SoT works best for structured, multi-point topics, but is unsuitable for tight sequential reasoning where step 2 depends strictly on step 1 output.

---

[⬅ Back to Prompt Engineering](./README.md) · [All topics](../README.md)
