---
title: "How do Rotary Position Embeddings (RoPE) and RoPE scaling work?"
id: 14
category: "LLM Fundamentals"
difficulty: "Advanced"
tags:
  - ai-engineering
  - llm-fundamentals
  - interview-questions
---

# How do Rotary Position Embeddings (RoPE) and RoPE scaling work?

**Short answer:** Rotary Position Embedding (RoPE) encodes positional information by multiplying query and key vectors by a rotation matrix based on token position, enabling self-attention to depend naturally on relative token distance; RoPE scaling interpolates or extrapolates these frequencies to expand context windows (e.g., from 4K to 128K) without full re-training.

## Detail

Unlike absolute positional embeddings added to token embeddings, RoPE applies a rotation to key ($K$) and query ($Q$) vectors in 2D vector slices:

$$R_{\Theta, m}^d x_m = \begin{pmatrix} \cos m\theta_1 & -\sin m\theta_1 \\ \sin m\theta_1 & \cos m\theta_1 \end{pmatrix} \begin{pmatrix} x_{m,1} \\ x_{m,2} \end{pmatrix}$$

### Key Advantages of RoPE

1. **Relative Distance Preservation:** The inner product between rotated query $R_m Q$ and rotated key $R_n K$ simplifies into a function of relative offset $(m - n)$, allowing models to naturally generalize distance across self-attention.
2. **Decay with Distance:** Attention weights naturally decrease as relative distance between tokens grows.

### RoPE Scaling Techniques for Extended Context

When fine-tuning a model trained on 4K context to handle 128K context:

- **Linear Scaling (Position Interpolation):** Scales positional indices down by factor $s = \frac{N_{new}}{N_{old}}$.
- **NTK-Aware Scaling:** Adjusts high-frequency and low-frequency components differently to preserve local precision while scaling global sequence context.
- **YaRN (Yet Another RoPE Extension):** Applies temperature scaling to attention softmax alongside frequency interpolation.

## Example

PyTorch snippet rotating a 2D slice with position index $m$:

```python
import torch

def apply_rope_2d(x: torch.Tensor, m: int, theta: float = 10000.0) -> torch.Tensor:
    # x shape: [batch, dim] where dim=2 for demonstration
    freq = 1.0 / (theta ** (0 / 2))
    angle = m * freq
    cos, sin = torch.cos(torch.tensor(angle)), torch.sin(torch.tensor(angle))

    x1, x2 = x[:, 0], x[:, 1]
    rot_x1 = x1 * cos - x2 * sin
    rot_x2 = x1 * sin + x2 * cos
    return torch.stack([rot_x1, rot_x2], dim=-1)

x = torch.tensor([[1.0, 0.0]])
print("Rotated vector at pos 5:", apply_rope_2d(x, m=5))
```

## Interview tips

- Note that RoPE is used by Llama 3, Mistral, Qwen 2, and most state-of-the-art open decoder models.
- Explain the distinction between extrapolation (out-of-distribution positions) and interpolation (scaling down position step sizes).

---

[⬅ Back to LLM Fundamentals](./README.md) · [All topics](../README.md)
