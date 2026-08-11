---
title: "How do state space models (SSMs) like Mamba compare to Transformer self-attention?"
id: 109
category: "LLM Fundamentals"
difficulty: "Advanced"
tags:
  - ai-engineering
  - llm-fundamentals
  - interview-questions
---

# How do state space models (SSMs) like Mamba compare to Transformer self-attention?

**Short answer:** State Space Models (SSMs) like Mamba replace quadratic $O(N^2)$ attention matrices with continuous-time hidden state updates ($h_t = A h_{t-1} + B x_t$), achieving $O(N)$ linear-time inference and constant $O(1)$ memory footprint per generated token.

## Detail

Transformers maintain a growing KV cache storing all past tokens. In contrast, Mamba models process context into a fixed-size recurrent hidden state vector.

```
Transformer: Input Token ──► KV Cache Grows with N ──► O(N^2) Prefill / O(N) Memory
Mamba SSM:   Input Token ──► Update Fixed State h_t ──► O(N) Prefill / O(1) Memory
```

### Mathematical Formulation

Mamba discretizes continuous differential equations into recurrent state updates:

$$h_t = \bar{A} h_{t-1} + \bar{B} x_t$$

$$y_t = C h_t$$

Where parameters $\bar{A}, \bar{B}, C$ are input-dependent functions (Selective State Space Mechanism), allowing the model to dynamically selectively filter out irrelevant context or retain critical facts.

| Attribute | Transformer | Mamba (Selective SSM) |
| --- | --- | --- |
| **Inference Time Complexity** | $O(N)$ per token | $O(1)$ per token |
| **Inference KV Memory** | Grows linearly $O(N)$ | Fixed constant $O(1)$ |
| **Training Mode** | Parallel via Attention | Parallel via Hardware-Aware Convolution |
| **Recall Density** | Exact multi-hop retrieval | Compressed state representation |

## Example

Conceptual Python comparison of state update vs KV cache append:

```python
# Mamba fixed-size state update (O(1) memory)
def mamba_step(x_t, h_prev, A_bar, B_bar, C):
    h_t = A_bar * h_prev + B_bar * x_t
    y_t = C * h_t
    return y_t, h_t # State size remains constant

# Transformer KV cache append (O(N) memory growth)
def transformer_step(x_t, kv_cache):
    kv_cache.append(x_t) # Cache grows indefinitely with N
    return compute_attention(x_t, kv_cache), kv_cache
```

## Interview tips

- Emphasize Mamba's hardware-aware algorithm (fusing state updates directly inside GPU SRAM to avoid HBM bandwidth bottlenecks).
- Discuss Hybrid Architectures (e.g. Jamba / Mamba-Transformer hybrids) that combine SSM throughput with Transformer retrieval precision.

## Related Concepts

- [[What is linear attention and how does it attempt to solve quadratic complexity?]] (`#107`): [What is linear attention and how does it attempt to solve quadratic complexity?](../llm-fundamentals/what-is-linear-attention-and-how-does-it-attempt-to-solve-quadratic-complexity.md)
- [[How does vLLM PagedAttention manage Virtual Memory Pages to eliminate KV cache fragmentation?]] (`#159`): [How does vLLM PagedAttention manage Virtual Memory Pages to eliminate KV cache fragmentation?](../ai-system-design/how-does-vllm-pagedattention-manage-virtual-memory-pages-to-eliminate-kv-cache-fragmentation.md)
- [[How do tensor parallelism (TP) and pipeline parallelism (PP) split large model weights across multi-GPU nodes?]] (`#157`): [How do tensor parallelism (TP) and pipeline parallelism (PP) split large model weights across multi-GPU nodes?](../ai-system-design/how-do-tensor-parallelism-tp-and-pipeline-parallelism-pp-split-large-model-weights-across-multi-gpu-nodes.md)

---

[⬅ Back to LLM Fundamentals](./README.md) · [All topics](../README.md)
