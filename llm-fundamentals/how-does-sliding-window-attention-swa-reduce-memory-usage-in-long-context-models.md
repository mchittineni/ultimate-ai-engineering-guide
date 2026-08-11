---
title: "How does sliding window attention (SWA) reduce memory usage in long-context models?"
id: 108
category: "LLM Fundamentals"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - llm-fundamentals
  - interview-questions
---

# How does sliding window attention (SWA) reduce memory usage in long-context models?

**Short answer:** Sliding Window Attention (SWA) restricts each token's attention scope to a fixed local window size $W$ (e.g. 4096 tokens), reducing KV cache memory and computation complexity from quadratic $O(N^2)$ to linear $O(N \cdot W)$, while enabling information to propagate across $L$ layers up to a theoretical receptive field of $L \times W$.

## Detail

Standard self-attention forces every token to attend to all prior tokens in the sequence length $N$.

```text
Full Attention (N=16K):    Token 16,000 attends to ALL 16,000 previous tokens. (Heavy Memory!)
Sliding Window (W=4K):     Token 16,000 attends ONLY to window [12,000 ... 16,000]. (Linear Memory!)
```

### Receptive Field Propagation Across Layers

Even though layer 1 has a restricted window $W$, stacking $L$ layers expands the effective receptive field:

$$\text{Receptive Field} = L \times W$$

A 32-layer model with a sliding window $W = 4096$ achieves an effective receptive field of $32 \times 4096 = 131,072$ tokens without ever allocating an $N \times N$ attention matrix.

| Mechanism                          | Attention Memory | KV Cache Growth | Max Theoretical Receptive Field |
| ---------------------------------- | ---------------- | --------------- | ------------------------------- |
| **Full Attention**                 | $O(N^2)$         | $O(N)$          | $N$                             |
| **Sliding Window Attention (SWA)** | $O(N \cdot W)$   | $O(W)$          | $L \times W$                    |

## Example

PyTorch concept for Sliding Window Attention mask generation:

```python
import torch

def create_sliding_window_mask(seq_len: int, window_size: int = 4) -> torch.Tensor:
    # Create causal mask
    causal_mask = torch.tril(torch.ones(seq_len, seq_len))
    # Create sliding window mask (zero out tokens beyond window W)
    window_mask = torch.triu(causal_mask, diagonal=-window_size + 1)
    # Positions outside window set to -infinity
    mask = torch.full((seq_len, seq_len), float('-inf'))
    mask[window_mask == 1] = 0.0
    return mask

print("Sliding Window Mask (0.0 = Attend, -inf = Blocked):\n", create_sliding_window_mask(6, window_size=3))
```

## Interview tips

- Discuss Mistral 7B as a prime example of Sliding Window Attention architecture.
- Highlight rolling buffer KV cache implementations that overwrite old tokens outside window $W$ to keep KV VRAM footprint constant.

## Related Concepts

- [[What is prefix caching (prompt caching) and how does it eliminate redundant KV computation?]] (`#152`): [What is prefix caching (prompt caching) and how does it eliminate redundant KV computation?](../ai-system-design/what-is-prefix-caching-prompt-caching-and-how-does-it-eliminate-redundant-kv-computation.md)
- [[How does Chunked Prefill prevent decoding latency spikes during concurrent batch processing?]] (`#156`): [How does Chunked Prefill prevent decoding latency spikes during concurrent batch processing?](../ai-system-design/how-does-chunked-prefill-prevent-decoding-latency-spikes-during-concurrent-batch-processing.md)
- [[How does contextual compression reduce context window token usage during RAG?]] (`#128`): [How does contextual compression reduce context window token usage during RAG?](../rag-and-vector-databases/how-does-contextual-compression-reduce-context-window-token-usage-during-rag.md)

---

[⬅ Back to LLM Fundamentals](./README.md) · [All topics](../README.md)
