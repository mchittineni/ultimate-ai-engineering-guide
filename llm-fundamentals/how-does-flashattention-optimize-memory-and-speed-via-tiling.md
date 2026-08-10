---
title: "How does FlashAttention optimize memory and speed via tiling?"
id: 55
category: "LLM Fundamentals"
difficulty: "Advanced"
tags:
  - ai-engineering
  - llm-fundamentals
  - interview-questions
---

# How does FlashAttention optimize memory and speed via tiling?

**Short answer:** FlashAttention restructures standard exact self-attention by tiling query, key, and value blocks to compute attention entirely within high-speed GPU SRAM, eliminating redundant read/write operations to slower High Bandwidth Memory (HBM) and reducing memory complexity from $O(N^2)$ to $O(N)$.

## Detail

Standard self-attention computes and materializes large intermediate matrices ($S = Q K^T$ and $P = \text{softmax}(S)$) in GPU High Bandwidth Memory (HBM).

### Memory IO Bottleneck

```
Standard Attention: GPU SRAM ◄──(Read/Write N^2 Matrices)──► GPU HBM (Slow ~2 TB/s)
FlashAttention:    GPU SRAM [Tiled Block Online Softmax] ──► Write Final Output O(N) to HBM
```

For sequence length $N=4096$, materializing $S$ and $P$ requires gigabytes of HBM memory traffic per layer.

### Core Technical Innovations in FlashAttention

1. **Tiling:** Partition inputs $Q, K, V$ into smaller sub-blocks that fit inside fast GPU SRAM (which runs at ~19 TB/s).
2. **Online Softmax:** Re-scale partial softmax results incrementally across tiles without storing full $N \times N$ attention weight matrices:

$$m_i^{(2)} = \max(m_i^{(1)}, \tilde{m}_i), \quad d_i^{(2)} = e^{m_i^{(1)} - m_i^{(2)}} d_i^{(1)} + e^{\tilde{m}_i - m_i^{(2)}} \tilde{d}_i$$

3. **Recomputation in Backward Pass:** During training, intermediate attention matrices are recomputed in SRAM during backpropagation rather than stored from the forward pass.

## Example

Conceptual Python illustration of online softmax update step:

```python
import torch

def online_softmax_chunk(prev_max, prev_sum, new_chunk_logits):
    chunk_max = torch.max(new_chunk_logits)
    new_max = torch.maximum(prev_max, chunk_max)
    
    # Rescale factor for previous sum
    rescale_prev = torch.exp(prev_max - new_max)
    rescale_new = torch.exp(new_chunk_logits - new_max)
    
    new_sum = prev_sum * rescale_prev + torch.sum(rescale_new)
    return new_max, new_sum
```

## Interview tips

- Emphasize that FlashAttention is an **exact** attention algorithm (not an approximation like Sparse Attention), producing mathematically identical outputs.
- Highlight FlashAttention-2/3 optimizations for FP8 precision and asynchronous GPU warp scheduling on NVIDIA Hopper (H100) GPUs.

---

[⬅ Back to LLM Fundamentals](./README.md) · [All topics](../README.md)
