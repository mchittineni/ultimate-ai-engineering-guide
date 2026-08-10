---
title: "What is LoRA rank r and alpha scaling factor?"
id: 73
category: "Fine-Tuning and Adaptation"
difficulty: "Beginner"
tags:
  - ai-engineering
  - fine-tuning-and-adaptation
  - interview-questions
---

# What is LoRA rank r and alpha scaling factor?

**Short answer:** Rank $r$ defines the inner dimension of low-rank adapter matrices $B \times A$, controlling the number of trainable parameters; alpha ($\alpha$) is a scaling hyperparameter that scales the adapter's update weight relative to base model weights during forward propagation.

## Detail

Low-Rank Adaptation (LoRA) decomposes weight updates $\Delta W$ into two low-rank matrices:

$$\Delta W = B \cdot A$$

Where $W_0 \in \mathbb{R}^{d \times k}$, $B \in \mathbb{R}^{d \times r}$, and $A \in \mathbb{R}^{r \times k}$ with $r \ll \min(d, k)$.

```text
Original Weight W_0 (d x k)  [FROZEN]
          +
Adapter Update (d x k)      =  (B [d x r]  *  A [r x k])  *  (alpha / r)
```

### The Scaling Equation

During forward propagation, the adapted forward pass is:

$$h = W_0 x + \frac{\alpha}{r} (B A) x$$

### Parameter Tuning Guidelines

- **Rank $r$:** Typical values are $r=8, 16, 32, 64$. Higher rank increases adapter expressiveness but increases VRAM usage.
- **Alpha ($\alpha$):** Standard heuristic sets $\alpha = 2 \times r$ (or $\alpha = r$). Keeping $\alpha$ constant when tuning $r$ avoids needing to retune the learning rate.

## Example

PyTorch LoRA scaling implementation:

```python
import torch
import torch.nn as nn

class LoRALayer(nn.Module):
    def __init__(self, in_dim: int, out_dim: int, r: int = 16, alpha: float = 32.0):
        super().__init__()
        self.r = r
        self.alpha = alpha
        self.scaling = alpha / r

        # Low-rank matrices
        self.lora_A = nn.Parameter(torch.randn(r, in_dim) * 0.01)
        self.lora_B = nn.Parameter(torch.zeros(out_dim, r))

    def forward(self, x: torch.Tensor, base_output: torch.Tensor) -> torch.Tensor:
        # Scale low-rank adapter output by (alpha / r)
        adapter_output = (x @ self.lora_A.T) @ self.lora_B.T
        return base_output + adapter_output * self.scaling
```

## Interview tips

- Explain why $\alpha / r$ scaling matters: it stabilizes training when experimenting with different values of rank $r$.
- Highlight that LoRA adapters can be merged back into base weights ($W = W_0 + \frac{\alpha}{r}BA$) for zero-latency inference deployment.

---

[⬅ Back to Fine-Tuning and Adaptation](./README.md) · [All topics](../README.md)
