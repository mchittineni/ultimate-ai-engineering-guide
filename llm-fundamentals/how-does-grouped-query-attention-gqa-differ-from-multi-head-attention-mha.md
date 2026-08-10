---
title: "How does Grouped-Query Attention (GQA) differ from Multi-Head Attention (MHA)?"
id: 2
category: "LLM Fundamentals"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - llm-fundamentals
  - interview-questions
---

# How does Grouped-Query Attention (GQA) differ from Multi-Head Attention (MHA)?

**Short answer:** Grouped-Query Attention (GQA) groups multiple query attention heads together to share a single Key-Value (KV) head, reducing the memory footprint of the KV cache during inference while maintaining model performance close to Multi-Head Attention (MHA).

## Detail

In standard Multi-Head Attention (MHA), every query head has its own corresponding Key head and Value head. If a model has 32 query heads, it also has 32 Key heads and 32 Value heads ($N_{Q} = N_{KV} = 32$).

As context window sizes scaled to 32K, 128K, or beyond, storing distinct K and V vectors for every head created severe GPU memory bottlenecks during multi-user serving.

Three main attention variants address this:

1. **Multi-Head Attention (MHA):** $N_{KV} = N_{Q}$. Maximum quality and expressiveness, but largest KV cache memory footprint.
2. **Multi-Query Attention (MQA):** $N_{KV} = 1$. All query heads share a single Key head and Value head. Minimum memory usage, but can degrade model reasoning quality.
3. **Grouped-Query Attention (GQA):** $1 < N_{KV} < N_{Q}$. Query heads are divided into $G$ groups, and all query heads within a group share one Key and Value head.

| Metric / Variant         | Multi-Head Attention (MHA)     | Grouped-Query Attention (GQA)                 | Multi-Query Attention (MQA)                    |
| ------------------------ | ------------------------------ | --------------------------------------------- | ---------------------------------------------- |
| **KV Heads ($N_{KV}$)**  | Equal to Query Heads ($N_{Q}$) | $N_{Q} / G$ (e.g., 8 KV heads for 32 Q heads) | 1 KV Head                                      |
| **KV Cache Size**        | $100\%$ (Baseline)             | Reduced by factor of $G$ (e.g., $25\%$)       | Reduced by factor of $N_{Q}$ (e.g., $3.125\%$) |
| **Inference Throughput** | Lower (Memory bound)           | Significantly Higher                          | Highest                                        |
| **Model Quality**        | Highest                        | Near MHA performance                          | Slight degradation on complex tasks            |

Llama 3 (8B, 70B), Mistral, and modern open foundation models adopt GQA with an 8:1 query-to-KV head ratio to maximize batch size and decoding speed on enterprise GPUs.

## Example

Architectural comparison of KV projection shapes in PyTorch:

```python
import torch
import torch.nn as nn

class GroupedQueryAttention(nn.Module):
    def __init__(self, d_model: int, n_q_heads: int, n_kv_heads: int):
        super().__init__()
        self.n_q_heads = n_q_heads
        self.n_kv_heads = n_kv_heads
        self.num_queries_per_kv = n_q_heads // n_kv_heads
        self.head_dim = d_model // n_q_heads

        self.q_proj = nn.Linear(d_model, n_q_heads * self.head_dim)
        self.k_proj = nn.Linear(d_model, n_kv_heads * self.head_dim)
        self.v_proj = nn.Linear(d_model, n_kv_heads * self.head_dim)

    def forward(self, x: torch.Tensor):
        b, s, _ = x.shape
        q = self.q_proj(x).view(b, s, self.n_q_heads, self.head_dim)
        k = self.k_proj(x).view(b, s, self.n_kv_heads, self.head_dim)
        v = self.v_proj(x).view(b, s, self.n_kv_heads, self.head_dim)

        # Expand K and V heads to match Q head count for attention calculation
        k = k.repeat_interleave(self.num_queries_per_kv, dim=2)
        v = v.repeat_interleave(self.num_queries_per_kv, dim=2)

        # Now shapes match for standard dot product attention
        return q, k, v
```

## Interview tips

- Highlight that GQA is an architectural change during training, whereas KV cache quantization (INT8/INT4) is a post-training optimization.
- Explain how GQA enables higher batch sizes in production serving frameworks (like vLLM or TensorRT-LLM), drastically increasing requests per second (RPS).

---

[⬅ Back to LLM Fundamentals](./README.md) · [All topics](../README.md)
