---
title: "What is the difference between causal and bidirectional self-attention?"
id: 102
category: "LLM Fundamentals"
difficulty: "Beginner"
tags:
  - ai-engineering
  - llm-fundamentals
  - interview-questions
---

# What is the difference between causal and bidirectional self-attention?

**Short answer:** Causal self-attention (used in autoregressive decoder models like GPT-4) applies an upper-triangular attention mask so token $i$ can only attend to past and current tokens ($j \le i$); bidirectional self-attention (used in encoder models like BERT) allows every token to attend to all past, present, and future tokens simultaneously.

## Detail

Self-attention computes dynamic context weights across sequences.

```
Bidirectional Attention (BERT):   Token i <──► Attends to ALL tokens (Past + Future)
Causal Masked Attention (GPT):   Token i ──► Attends ONLY to past tokens (<= i)
```

### Mathematical Difference in Attention Matrix

Standard Self-Attention:

$$\text{Attention}(Q, K, V) = \text{Softmax}\left(\frac{Q K^T}{\sqrt{d_k}} + M\right) V$$

For Causal Attention, mask matrix $M_{ij} = -\infty$ for $j > i$, driving Softmax probabilities for future tokens to exact zero.

| Model Type | Attention Type | Primary Use Cases | Examples |
| --- | --- | --- | --- |
| **Encoder-only** | Bidirectional | Text classification, embedding generation, NER | BERT, RoBERTa, DeBERTa |
| **Decoder-only** | Causal (Masked) | Text generation, code generation, reasoning | GPT-4o, Llama 3, Qwen 2.5 |

## Example

PyTorch implementation of causal attention masking:

```python
import torch

seq_len = 4
scores = torch.randn(seq_len, seq_len)

# Upper triangular mask set to -infinity
causal_mask = torch.triu(torch.full((seq_len, seq_len), float('-inf')), diagonal=1)
masked_scores = scores + causal_mask
attn_weights = torch.softmax(masked_scores, dim=-1)

print("Causal Attention Weights (Future tokens zeroed out):\n", attn_weights)
```

## Interview tips

- Emphasize why decoder-only models use causal attention: autoregressive generation predicts the next token $t+1$ without peeking at future targets.
- Highlight Prefix LM attention variants that combine bidirectional attention on system prompts with causal attention on outputs.

---

[⬅ Back to LLM Fundamentals](./README.md) · [All topics](../README.md)
