---
title: "What is KV Cache and how does it speed up inference?"
id: 1
category: "LLM Fundamentals"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - llm-fundamentals
  - interview-questions
---

# What is KV Cache and how does it speed up inference?

**Short answer:** Key-Value (KV) Cache stores the precomputed Key and Value vector representations of previously processed tokens in memory during autoregressive decoding, preventing redundant matrix multiplications for past tokens at every new token generation step.

## Detail

In autoregressive Large Language Models (LLMs), text generation happens token-by-token. To generate token $N+1$, the self-attention mechanism needs to calculate attention scores between the query vector $Q_{N+1}$ and the key/value vectors of all preceding tokens ($K_{1..N+1}$ and $V_{1..N+1}$).

Without KV Caching:

- At step $N$, the model computes $K_1, \dots, K_N$ and $V_1, \dots, V_N$.
- At step $N+1$, the model would recompute $K_1, \dots, K_{N+1}$ and $V_1, \dots, V_{N+1}$ from scratch.
- Time complexity per step grows quadratically with sequence length ($O(N^2)$ flops over the generation loop).

With KV Caching:

- The model computes and stores $K_i, V_i$ for past tokens in GPU memory.
- At step $N+1$, the model computes ONLY $Q_{N+1}, K_{N+1}, V_{N+1}$ for the new token, appends $K_{N+1}$ and $V_{N+1}$ to the cache, and computes attention against the stored keys and values.
- Time complexity per step drops from $O(N)$ projection operations to $O(1)$ new projections + $O(N)$ memory fetch and attention dot product.

### Memory Impact

While KV caching drastically speeds up generation (reducing latency by up to 10x), it shifts inference from compute-bound to memory-capacity bound. For a model with $L$ layers, $H$ attention heads, head dimension $d_k$, sequence length $S$, batch size $B$, and precision $P$ bytes:

$$\text{KV Cache Size (Bytes)} = 2 \times B \times S \times L \times H \times d_k \times P$$

For Llama-3-70B running float16 ($P=2$) with a 4K context window and batch size 1, KV cache alone consumes ~1.3 GB of GPU VRAM per stream.

## Example

Below is a conceptual Python implementation demonstrating autoregressive decoding with and without KV caching:

```python
import torch
import torch.nn as nn

class CausalSelfAttentionWithKVCache(nn.Module):
    def __init__(self, d_model: int, n_heads: int):
        super().__init__()
        self.d_model = d_model
        self.n_heads = n_heads
        self.head_dim = d_model // n_heads

        self.q_proj = nn.Linear(d_model, d_model)
        self.k_proj = nn.Linear(d_model, d_model)
        self.v_proj = nn.Linear(d_model, d_model)
        self.out_proj = nn.Linear(d_model, d_model)

    def forward(self, x: torch.Tensor, kv_cache=None):
        # x shape: (batch_size, seq_len, d_model)
        b, seq_len, _ = x.shape

        # Project new token input
        q = self.q_proj(x).view(b, seq_len, self.n_heads, self.head_dim).transpose(1, 2)
        k = self.k_proj(x).view(b, seq_len, self.n_heads, self.head_dim).transpose(1, 2)
        v = self.v_proj(x).view(b, seq_len, self.n_heads, self.head_dim).transpose(1, 2)

        if kv_cache is not None:
            prev_k, prev_v = kv_cache
            k = torch.cat([prev_k, k], dim=2)
            v = torch.cat([prev_v, v], dim=2)

        new_kv_cache = (k, v)

        # Scaled dot-product attention
        scores = torch.matmul(q, k.transpose(-2, -1)) / (self.head_dim ** 0.5)
        attn_weights = torch.softmax(scores, dim=-1)
        output = torch.matmul(attn_weights, v)

        output = output.transpose(1, 2).contiguous().view(b, seq_len, self.d_model)
        return self.out_proj(output), new_kv_cache
```

## Interview tips

- Always distinguish prefill phase (compute-bound batch processing of prompt tokens) from decoding phase (memory-bandwidth bound single token generation).
- Mention Grouped-Query Attention (GQA) and Multi-Query Attention (MQA) as key architectural optimizations designed specifically to shrink KV cache size.
- Be prepared to discuss PagedAttention (vLLM) as the standard production solution for memory fragmentation caused by dynamic KV cache allocation.

---

[⬅ Back to LLM Fundamentals](./README.md) · [All topics](../README.md)
