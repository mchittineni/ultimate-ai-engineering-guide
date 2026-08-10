---
title: "How does Multi-Query Attention (MQA) differ from Multi-Head Attention?"
id: 54
category: "LLM Fundamentals"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - llm-fundamentals
  - interview-questions
---

# How does Multi-Query Attention (MQA) differ from Multi-Head Attention?

**Short answer:** Multi-Query Attention (MQA) uses multiple Query heads but shares a single Key head and single Value head across all Query heads, reducing the KV cache memory footprint by $N_{heads}$ factor compared to Multi-Head Attention (MHA).

## Detail

In standard Multi-Head Attention (MHA), every query head has a distinct key head and value head ($N_Q = N_{KV} = 32$).

Multi-Query Attention (MQA) drastically compresses KV memory:

$$\text{MHA: } N_{KV} = N_Q \quad \text{vs} \quad \text{MQA: } N_{KV} = 1$$

| Attention Variant                 | Query Heads ($N_Q$) | Key/Value Heads ($N_{KV}$) | KV Cache Memory Savings   | Quality Impact                        |
| --------------------------------- | ------------------- | -------------------------- | ------------------------- | ------------------------------------- |
| **Multi-Head Attention (MHA)**    | 32                  | 32                         | Baseline (100%)           | Highest expressiveness                |
| **Multi-Query Attention (MQA)**   | 32                  | 1                          | ~96.8% reduction ($1/32$) | Higher risk of reasoning degradation  |
| **Grouped-Query Attention (GQA)** | 32                  | 8                          | ~75% reduction ($8/32$)   | Optimal quality/throughput compromise |

## Example

PyTorch shape comparison between MHA, MQA, and GQA:

```python
import torch

batch, seq_len, d_model = 2, 512, 4096
n_q_heads = 32

# MHA: 32 K and V heads
k_mha = torch.randn(batch, seq_len, 32, d_model // 32)

# MQA: 1 K and V head (shared across all 32 Q heads)
k_mqa = torch.randn(batch, seq_len, 1, d_model // 32)

print("MHA Key Tensor Shape:", k_mha.shape)
print("MQA Key Tensor Shape:", k_mqa.shape)
```

## Interview tips

- Highlight that MQA dramatically improves decoding speed on memory-bandwidth bound inference servers, but can slightly hurt complex reasoning.
- Mention GQA as the modern evolution adopted by Llama 3 that balances MHA quality with MQA memory efficiency.

---

[⬅ Back to LLM Fundamentals](./README.md) · [All topics](../README.md)
