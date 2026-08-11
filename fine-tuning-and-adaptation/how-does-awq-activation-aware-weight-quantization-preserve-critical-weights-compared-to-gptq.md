---
title: "How does AWQ (Activation-aware Weight Quantization) preserve critical weights compared to GPTQ?"
id: 148
category: "Fine-Tuning and Adaptation"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - fine-tuning-and-adaptation
  - interview-questions
---

# How does AWQ (Activation-aware Weight Quantization) preserve critical weights compared to GPTQ?

**Short answer:** AWQ (Activation-aware Weight Quantization) protects top 1% critical weights from 4-bit quantization distortion by observing activation magnitude distributions during calibration, scaling salient weight channels to maintain floating-point precision where it matters most.

## Detail

Naive 4-bit uniform quantization quantizes all weights equally, degrading perplexity on complex reasoning tasks.

GPTQ quantizes weight columns sequentially by solving inverse Hessian error compensation equations.

AWQ observes that **not all weights are equally important**:

```
Observation: 1% of weight channels correspond to 99% of large activation magnitudes.

AWQ Strategy:
1. Identify salient weight channels via activation norm ||X||.
2. Protect salient channels S by multiplying weights W by per-channel scale s > 1.
3. Quantize scaled weights -> Preserves high precision on critical activation channels.
```

### Key Differences

| Feature | GPTQ | AWQ |
| --- | --- | --- |
| **Quantization Basis** | Second-order inverse Hessian weight error | Activation magnitude norms $\|X\|$ |
| **Outlier Protection** | Error compensation across matrix columns | Per-channel activation scaling $s \cdot W$ |
| **Generalization** | Prone to overfitting calibration dataset | Superior generalization across out-of-domain prompts |
| **Inference Hardware Speed** | High | Ultra-fast (Native vLLM/TRT-LLM 4-bit kernels) |

## Example

AWQ quantization loading in vLLM Python inference server:

```python
from vllm import LLM, SamplingParams

# Load pre-quantized INT4 AWQ model directly onto GPU
llm = LLM(
    model="TheBloke/Llama-2-70B-Chat-AWQ",
    quantization="awq",
    tensor_parallel_size=2
)

params = SamplingParams(temperature=0.1, max_tokens=100)
outputs = llm.generate(["Explain AWQ quantization vs GPTQ:"], params)
print(outputs[0].outputs[0].text)
```

## Interview tips

- Emphasize that AWQ is hardware-friendly: because it applies per-channel scale factors without sparse matrix structures, it executes with high throughput on NVIDIA Tensor Cores.
- Highlight AWQ as the default 4-bit quantization format supported in vLLM for production GPU serving.

## Related Concepts

- [[How does GGUF format enable quantization and CPU/GPU offloading in llama.cpp?]] (`#147`): [How does GGUF format enable quantization and CPU/GPU offloading in llama.cpp?](../fine-tuning-and-adaptation/how-does-gguf-format-enable-quantization-and-cpu-gpu-offloading-in-llama-cpp.md)
- [[How do tensor parallelism (TP) and pipeline parallelism (PP) split large model weights across multi-GPU nodes?]] (`#157`): [How do tensor parallelism (TP) and pipeline parallelism (PP) split large model weights across multi-GPU nodes?](../ai-system-design/how-do-tensor-parallelism-tp-and-pipeline-parallelism-pp-split-large-model-weights-across-multi-gpu-nodes.md)
- [[How does vLLM PagedAttention manage Virtual Memory Pages to eliminate KV cache fragmentation?]] (`#159`): [How does vLLM PagedAttention manage Virtual Memory Pages to eliminate KV cache fragmentation?](../ai-system-design/how-does-vllm-pagedattention-manage-virtual-memory-pages-to-eliminate-kv-cache-fragmentation.md)

---

[⬅ Back to Fine-Tuning and Adaptation](./README.md) · [All topics](../README.md)
