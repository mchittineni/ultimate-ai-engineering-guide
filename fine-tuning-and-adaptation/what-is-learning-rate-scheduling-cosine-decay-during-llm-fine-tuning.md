---
title: "What is learning rate scheduling (cosine decay) during LLM fine-tuning?"
id: 142
category: "Fine-Tuning and Adaptation"
difficulty: "Beginner"
tags:
  - ai-engineering
  - fine-tuning-and-adaptation
  - interview-questions
---

# What is learning rate scheduling (cosine decay) during LLM fine-tuning?

**Short answer:** Learning rate scheduling dynamically adjusts the optimizer's learning rate ($\eta$) during training; cosine decay warms up the learning rate linearly for initial steps before gradually decaying it along a cosine curve to a small minimum learning rate, stabilizing LLM convergence.

## Detail

Constant learning rates cause training instability: too high a learning rate early on causes loss divergence, while too high a learning rate late in training prevents the model from settling into optimal loss minima.

```text
Learning Rate (η)
  ▲
  │     /─── Cosine Decay Curve ───\
  │    /                            \
  │   / (Linear Warmup)              \___ (Min LR)
  └───────────────────────────────────────────────► Training Steps
```

### The Cosine Decay Formula with Warmup

For step $t$, warmup steps $T_{warmup}$, and total steps $T_{total}$:

$$\eta_t = \eta_{min} + \frac{1}{2}(\eta_{max} - \eta_{min}) \left(1 + \cos\left(\frac{t - T_{warmup}}{T_{total} - T_{warmup}} \pi\right)\right)$$

### Why Cosine Decay is Preferred

- **Warmup Phase:** Prevents large initial gradients from destabilizing pre-trained weight matrices.
- **Smooth Decay:** Cosine curvature decays slower than exponential decay mid-training, maintaining optimization velocity before gently dampening updates near convergence.

## Example

PyTorch Cosine Annealing scheduler configuration pattern:

```python
import torch
from torch.optim.lr_scheduler import CosineAnnealingLR

optimizer = torch.optim.AdamW([torch.nn.Parameter(torch.randn(10))], lr=2e-5)
scheduler = CosineAnnealingLR(optimizer, T_max=1000, eta_min=2e-6)

# Simulate training loop
for step in range(5):
    optimizer.step()
    scheduler.step()
    print(f"Step {step+1} Learning Rate: {scheduler.get_last_lr()[0]:.2e}")
```

## Interview tips

- Emphasize typical LLM fine-tuning learning rates: $1\text{e-}4 - 3\text{e-}4$ for LoRA fine-tuning vs $1\text{e-}5 - 2\text{e-}5$ for full parameter SFT.
- Discuss warmup ratios (typically $3\% - 5\%$ of total training steps).

## Related Concepts

- [[What is gradient accumulation and how does it simulate larger batch sizes on small GPUs?]] (`#143`): [What is gradient accumulation and how does it simulate larger batch sizes on small GPUs?](../fine-tuning-and-adaptation/what-is-gradient-accumulation-and-how-does-it-simulate-larger-batch-sizes-on-small-gpus.md)
- [[How does DeepSpeed ZeRO stage 1, 2, and 3 partition optimizer states, gradients, and parameters?]] (`#150`): [How does DeepSpeed ZeRO stage 1, 2, and 3 partition optimizer states, gradients, and parameters?](../fine-tuning-and-adaptation/how-does-deepspeed-zero-stage-1-2-and-3-partition-optimizer-states-gradients-and-parameters.md)

---

[⬅ Back to Fine-Tuning and Adaptation](./README.md) · [All topics](../README.md)
