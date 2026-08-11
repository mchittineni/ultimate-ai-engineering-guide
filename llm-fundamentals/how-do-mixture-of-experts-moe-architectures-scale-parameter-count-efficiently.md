---
title: "How do Mixture of Experts (MoE) architectures scale parameter count efficiently?"
id: 106
category: "LLM Fundamentals"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - llm-fundamentals
  - interview-questions
---

# How do Mixture of Experts (MoE) architectures scale parameter count efficiently?

**Short answer:** Mixture of Experts (MoE) architectures scale parameter capacity by replacing dense Feed-Forward Network (FFN) layers with multiple sparse "expert" subnetworks, using a learned router (gating network) to route each token to a small subset of top-$K$ experts (e.g. 2 out of 8), increasing total parameters without increasing FLOPs per token.

## Detail

Dense Transformers route every token through 100% of model parameters.

MoE models (e.g. Mixtral 8x7B, DeepSeek-V3) decouple total parameter capacity from active inference compute:

```
Token Hidden State ──► [Top-K Router / Gating Network]
                             │
       ┌─────────────────────┼─────────────────────┐
       ▼ (Routed to Expert 1)  ▼ (Routed to Expert 4)  ▼ (Skipped Experts 2, 3, 5-8)
   [Expert FFN 1]          [Expert FFN 4]
       │                     │
       └─────────────────────┴─────────────────────► Weighted Sum Combination
```

### Key MoE Parameters

- **Total Parameters:** Sum of all parameters across all experts (e.g. 47B for Mixtral 8x7B).
- **Active Parameters:** Parameters activated per token pass (e.g. 13B for Mixtral 8x7B).
- **Top-$K$ Routing:** Number of experts selected per token (typically $K = 2$).

## Example

PyTorch implementation concept for Sparse MoE Gating Layer:

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class SparseMoEGating(nn.Module):
    def __init__(self, d_model=512, num_experts=8, top_k=2):
        super().__init__()
        self.router = nn.Linear(d_model, num_experts)
        self.top_k = top_k

    def forward(self, x):
        # Calculate router logits
        logits = self.router(x)
        # Select top-k experts and compute Softmax weights
        top_k_logits, top_k_indices = torch.topk(logits, self.top_k, dim=-1)
        top_k_probs = F.softmax(top_k_logits, dim=-1)
        return top_k_probs, top_k_indices
```

## Interview tips

- Discuss Aux Loss (Auxiliary Load Balancing Loss) used during training to prevent router collapse where 1-2 popular experts receive all token traffic while others remain untrained.
- Explain VRAM memory footprint trade-offs: MoE models require hosting all 47B parameters in GPU memory despite only executing 13B FLOPs per token.

---

[⬅ Back to LLM Fundamentals](./README.md) · [All topics](../README.md)
