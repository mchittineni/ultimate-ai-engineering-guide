---
title: "How do tensor parallelism (TP) and pipeline parallelism (PP) split large model weights across multi-GPU nodes?"
id: 157
category: "AI System Design"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - ai-system-design
  - interview-questions
---

# How do tensor parallelism (TP) and pipeline parallelism (PP) split large model weights across multi-GPU nodes?

**Short answer:** Tensor Parallelism (TP) splits individual weight matrices (QKV projections, FFN layers) intra-layer across multiple GPUs within a single node using high-speed NVLink; Pipeline Parallelism (PP) partitions layers sequentially inter-node across multiple server nodes, passing intermediate hidden states through a multi-stage pipeline.

## Detail

Fitting 70B to 405B parameter models in GPU memory exceeds single-GPU VRAM capacity (e.g. 80GB H100).

```text
Tensor Parallelism (TP=2) - Intra-Layer Split:
Matrix W (4096 x 4096) ──► Split Column-wise ──► GPU 0: W1 (4096 x 2048)
                                              ──► GPU 1: W2 (4096 x 2048)
(Requires AllReduce sync over NVLink after every layer)

Pipeline Parallelism (PP=2) - Inter-Layer Split:
GPU 0 (Node A): Transformer Layers 1 to 16  ──► Passes Hidden State via Network
GPU 1 (Node B): Transformer Layers 17 to 32
```

### Core Comparison

| Dimension                      | Tensor Parallelism (TP)                  | Pipeline Parallelism (PP)                       |
| ------------------------------ | ---------------------------------------- | ----------------------------------------------- |
| **Partition Unit**             | Individual Linear Weight Matrices ($W$)  | Whole Transformer Layers (Blocks)               |
| **Communication Interconnect** | High-speed Intra-Node NVLink (~900 GB/s) | Inter-Node InfiniBand / Ethernet (~50-100 GB/s) |
| **Communication Frequency**    | High (AllReduce per attention/FFN layer) | Low (Handshake at stage boundaries)             |
| **Primary Bottleneck**         | Memory Bandwidth & NVLink Latency        | Pipeline Bubble (GPU Idle Time)                 |

## Example

Conceptual Python PyTorch Tensor Parallelism column-wise linear split:

```python
import torch
import torch.nn as nn

class TensorParallelColumnLinear(nn.Module):
    def __init__(self, in_features: int, out_features: int, tp_world_size: int = 2):
        super().__init__()
        # Split output dimension across GPUs
        self.tp_out_features = out_features // tp_world_size
        self.weight = nn.Parameter(torch.randn(self.tp_out_features, in_features))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Each GPU computes half of the output projection
        return x @ self.weight.T # Local MatMul
```

## Interview tips

- Explain 3D Parallelism: combining Tensor Parallelism (TP), Pipeline Parallelism (PP), and Data Parallelism (DP) / ZeRO to train trillion-parameter models across thousands of GPUs.
- Discuss how Pipeline Bubbles (1F1B schedule) reduce idle GPU waiting time during pipeline execution.

## Related Concepts

- [[How does DeepSpeed ZeRO stage 1, 2, and 3 partition optimizer states, gradients, and parameters?]] (`#150`): [How does DeepSpeed ZeRO stage 1, 2, and 3 partition optimizer states, gradients, and parameters?](../fine-tuning-and-adaptation/how-does-deepspeed-zero-stage-1-2-and-3-partition-optimizer-states-gradients-and-parameters.md)
- [[How to lead an ambiguous AI system design interview from requirements to architecture?]] (`#196`): [How to lead an ambiguous AI system design interview from requirements to architecture?](../interview-experience/how-to-lead-an-ambiguous-ai-system-design-interview-from-requirements-to-architecture.md)

---

[⬅ Back to AI System Design](./README.md) · [All topics](../README.md)
