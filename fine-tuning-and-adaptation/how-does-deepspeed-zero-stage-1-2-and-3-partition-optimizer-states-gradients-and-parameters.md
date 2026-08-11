---
title: "How does DeepSpeed ZeRO stage 1, 2, and 3 partition optimizer states, gradients, and parameters?"
id: 150
category: "Fine-Tuning and Adaptation"
difficulty: "Advanced"
tags:
  - ai-engineering
  - fine-tuning-and-adaptation
  - interview-questions
---

# How does DeepSpeed ZeRO stage 1, 2, and 3 partition optimizer states, gradients, and parameters?

**Short answer:** DeepSpeed ZeRO (Zero Redundancy Optimizer) eliminates memory redundancy across data-parallel GPU nodes by partitioning optimizer states (ZeRO-1), gradients (ZeRO-2), and model parameters (ZeRO-3), enabling training of trillion-parameter models without full parameter duplication.

## Detail

In standard Data Parallelism (DP), every GPU holds a 100% duplicate copy of model parameters, gradients, and Adam optimizer states (FP32 master weights, momentum, variance).

```
Standard DP: GPU 0 [Parameters + Gradients + Optimizer States] (Redundant on GPU 1, GPU 2...)

ZeRO-1 (Optimizer State Partitioning):
GPU 0 [Params] [Grads] [Opt Part 0] | GPU 1 [Params] [Grads] [Opt Part 1]

ZeRO-2 (Gradient + Optimizer State Partitioning):
GPU 0 [Params] [Grad Part 0] [Opt Part 0] | GPU 1 [Params] [Grad Part 1] [Opt Part 1]

ZeRO-3 (Parameter + Gradient + Optimizer State Partitioning):
GPU 0 [Param Part 0] [Grad Part 0] [Opt Part 0] | GPU 1 [Param Part 1] [Grad Part 1] [Opt Part 1]
```

### Memory Footprint Reduction Matrix

For model with $P$ parameters trained in FP16/BF16 with Adam optimizer:

| ZeRO Stage | Partitioned Components | Total Memory Footprint per GPU | Communication Overhead |
| --- | --- | --- | --- |
| **Baseline DP** | None (Fully Replicated) | $2P (\text{Weights}) + 2P (\text{Grads}) + 12P (\text{Adam}) = 16P$ | Baseline AllReduce |
| **ZeRO-1** | Optimizer States ($P_{opt}$) | $4P + \frac{12P}{N_{gpus}}$ | Same as Baseline |
| **ZeRO-2** | Optimizer States + Gradients ($P_{grad}$) | $2P + \frac{14P}{N_{gpus}}$ | Same as Baseline |
| **ZeRO-3** | Optimizer States + Gradients + Parameters ($P_{param}$) | $\frac{16P}{N_{gpus}}$ | ~1.5x AllGather overhead |

## Example

DeepSpeed configuration JSON for ZeRO-3 with CPU offloading:

```json
{
  "train_batch_size": 32,
  "zero_optimization": {
    "stage": 3,
    "offload_optimizer": {
      "device": "cpu",
      "pin_memory": true
    },
    "offload_param": {
      "device": "cpu",
      "pin_memory": true
    },
    "overlap_comm": true,
    "contiguous_gradients": true
  }
}
```

## Interview tips

- Highlight memory math: training a 70B parameter model requires ~1.12 TB of GPU memory in standard DP, but only ~14 GB per GPU when using ZeRO-3 across 64 GPUs.
- Discuss ZeRO-Infinity for NVMe offloading.

## Related Concepts

- [[What is gradient accumulation and how does it simulate larger batch sizes on small GPUs?]] (`#143`): [What is gradient accumulation and how does it simulate larger batch sizes on small GPUs?](../fine-tuning-and-adaptation/what-is-gradient-accumulation-and-how-does-it-simulate-larger-batch-sizes-on-small-gpus.md)
- [[How do tensor parallelism (TP) and pipeline parallelism (PP) split large model weights across multi-GPU nodes?]] (`#157`): [How do tensor parallelism (TP) and pipeline parallelism (PP) split large model weights across multi-GPU nodes?](../ai-system-design/how-do-tensor-parallelism-tp-and-pipeline-parallelism-pp-split-large-model-weights-across-multi-gpu-nodes.md)

---

[⬅ Back to Fine-Tuning and Adaptation](./README.md) · [All topics](../README.md)
