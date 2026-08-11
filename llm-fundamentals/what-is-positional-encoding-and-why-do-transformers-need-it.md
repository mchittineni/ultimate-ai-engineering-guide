---
title: "What is positional encoding and why do Transformers need it?"
id: 105
category: "LLM Fundamentals"
difficulty: "Beginner"
tags:
  - ai-engineering
  - llm-fundamentals
  - interview-questions
---

# What is positional encoding and why do Transformers need it?

**Short answer:** Positional encoding injects word-order position information into token embeddings; Transformers need it because self-attention matrix operations ($\text{Softmax}(QK^T)V$) are permutation invariant, meaning a Transformer processes "Dog bites man" and "Man bites dog" identically without explicit position signals.

## Detail

Unlike Recurrent Neural Networks (RNNs) that process tokens sequentially step-by-step, self-attention processes all tokens in parallel.

```
Without Positional Encoding:
"Dog bites man" ──► [Self-Attention Set Operation] ──► Identical to "Man bites dog"

With Positional Encoding:
Token Embedding E_i + Position Encoding P_i ──► Position-Aware Attention Representation
```

### Evolution of Positional Encodings

1. **Absolute Sinusoidal (Attention is All You Need):** Static sine/cosine wave functions added to input embeddings.
2. **Learned Absolute Position Embeddings:** Trainable positional vectors (GPT-2, BERT).
3. **Rotary Position Embeddings (RoPE):** Multiplies Query and Key vectors by a rotation matrix based on token index $m$, dominating modern LLMs (Llama 3, Qwen 2.5).

## Example

PyTorch implementation concept for Sinusoidal Positional Encoding:

```python
import torch
import math

def get_sinusoidal_positional_encoding(seq_len: int, d_model: int) -> torch.Tensor:
    pe = torch.zeros(seq_len, d_model)
    position = torch.arange(0, seq_len, dtype=torch.float).unsqueeze(1)
    div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
    
    pe[:, 0::2] = torch.sin(position * div_term)
    pe[:, 1::2] = torch.cos(position * div_term)
    return pe

pe = get_sinusoidal_positional_encoding(seq_len=4, d_model=512)
print("Positional Encoding Matrix Shape:", pe.shape)
```

## Interview tips

- Contrast Absolute Positional Embeddings with Rotary Position Embeddings (RoPE).
- Discuss RoPE context extension techniques (YaRN, NTK-aware scaling).

---

[⬅ Back to LLM Fundamentals](./README.md) · [All topics](../README.md)
