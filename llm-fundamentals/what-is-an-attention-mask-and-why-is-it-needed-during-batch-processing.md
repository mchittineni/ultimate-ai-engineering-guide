---
title: "What is an attention mask and why is it needed during batch processing?"
id: 104
category: "LLM Fundamentals"
difficulty: "Beginner"
tags:
  - ai-engineering
  - llm-fundamentals
  - interview-questions
---

# What is an attention mask and why is it needed during batch processing?

**Short answer:** An attention mask is a binary tensor (`1` for real tokens, `0` for padding tokens) that instructs the self-attention mechanism to ignore zero-padding tokens added when batching sequences of varying lengths, preventing dummy pad tokens from influencing sequence context calculations.

## Detail

GPU hardware requires batch inputs formatted into uniform rectangular tensor shapes ($B \times N \times d$).

When sequences in a batch have different token lengths, shorter sequences are padded with zero tokens.

```
Batch Item 1 (Length 3): ["AI", "Is", "Great"]       ──► [1, 1, 1]  (No Padding)
Batch Item 2 (Length 2): ["Hello", "World", <PAD>] ──► [1, 1, 0]  (Attention Mask Zeroes <PAD>)
```

### How Attention Mask Modifies Self-Attention

$$\text{Attention}(Q, K, V) = \text{Softmax}\left(\frac{Q K^T}{\sqrt{d_k}} + M_{\text{pad}}\right) V$$

Where padding mask $M_{\text{pad}} = -\infty$ at padding token positions, ensuring Softmax assigns zero attention weight to padding tokens.

## Example

PyTorch implementation of batch attention masking:

```python
import torch

# Batch of 2 sequences (Max length 4)
# 1 = Real token, 0 = Padding token
attention_mask = torch.tensor([
    [1, 1, 1, 1], # Seq 1: 4 real tokens
    [1, 1, 0, 0]  # Seq 2: 2 real tokens, 2 pad tokens
])

raw_scores = torch.randn(2, 4)
# Add large negative value to padding positions
masked_scores = raw_scores.masked_fill(attention_mask == 0, -1e9)
probs = torch.softmax(masked_scores, dim=-1)

print("Attention Probabilities for Padded Batch:\n", probs)
```

## Interview tips

- Highlight flash attention optimizations (FlashAttention 2/3) that eliminate padding tokens altogether using varlen unpadded memory layouts.
- Distinguish between padding attention masks and causal autoregressive masks.

---

[⬅ Back to LLM Fundamentals](./README.md) · [All topics](../README.md)
