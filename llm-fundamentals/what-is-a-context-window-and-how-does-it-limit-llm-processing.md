---
title: "What is a context window and how does it limit LLM processing?"
id: 53
category: "LLM Fundamentals"
difficulty: "Beginner"
tags:
  - ai-engineering
  - llm-fundamentals
  - interview-questions
---

# What is a context window and how does it limit LLM processing?

**Short answer:** A context window is the maximum number of total tokens (prompt input + completion output combined) that an LLM can attend to in a single forward pass, bounded by GPU memory capacity and positional encoding bounds.

## Detail

The context window (e.g. 4K, 32K, 128K, or 1M tokens) dictates the maximum operational horizon of a model:

```
┌──────────────────────────────────────────────────────────┐
│                   TOTAL CONTEXT WINDOW                   │
├──────────────────────────────┬───────────────────────────┤
│ Input Prompt Tokens (System, │ Max Output Generation     │
│ Few-shot, RAG context)       │ Completion Tokens         │
└──────────────────────────────┴───────────────────────────┘
```

### Core Limits Enforced by Context Windows

1. **Quadratic Attention Bottleneck:** Standard self-attention compute scales quadratically $O(N^2)$ with sequence length $N$ during prefill.
2. **KV Cache VRAM Memory Footprint:** Longer context windows require exponentially larger GPU VRAM reserves to store Key-Value tensors for active user streams.
3. **Information Retrieval Loss ("Lost in the Middle"):** As context windows scale to 128K+, LLMs struggle to recall details placed in the middle of long prompts compared to the beginning and end.

## Example

Context allocation check snippet in Python:

```python
def check_context_window(prompt_tokens: int, max_output_tokens: int, model_limit: int = 32768) -> bool:
    total_tokens = prompt_tokens + max_output_tokens
    if total_tokens > model_limit:
        raise ValueError(
            f"Context window exceeded: Requested {total_tokens} tokens ({prompt_tokens} prompt + "
            f"{max_output_tokens} output), but model limit is {model_limit}."
        )
    return True

check_context_window(prompt_tokens=30000, max_output_tokens=4000, model_limit=32768)
```

## Interview tips

- Emphasize that context length limits apply to **tokens**, not characters or words (1 token $\approx$ 0.75 English words).
- Discuss strategies for managing context limits: document chunking, prompt truncation, dynamic summarization, and RAG.

---

[⬅ Back to LLM Fundamentals](./README.md) · [All topics](../README.md)
