---
title: "What is quantization and how do INT8 and INT4 reduce LLM footprint?"
id: 28
category: "Fine-Tuning and Adaptation"
difficulty: "Beginner"
tags:
  - ai-engineering
  - fine-tuning-and-adaptation
  - interview-questions
---

# What is quantization and how do INT8 and INT4 reduce LLM footprint?

**Short answer:** Quantization maps high-precision floating-point weights and activations (FP16 or BF16) to lower-precision integer representations (INT8 or INT4), reducing GPU memory footprint by up to 75% and increasing memory bandwidth efficiency with minimal loss in model accuracy.

## Detail

Standard foundation models are trained in 16-bit precision (FP16 or BF16), requiring 2 bytes of VRAM per parameter. A 70B parameter model requires $\sim 140\text{ GB}$ of VRAM just to load model weights into memory.

### Precision Comparison

| Format | Bits per Weight | Bytes per Weight | VRAM for 70B Model | Perplexity Loss |
| --- | --- | --- | --- | --- |
| **FP16 / BF16** | 16 bits | 2 bytes | ~140 GB | Baseline |
| **INT8 (8-bit)** | 8 bits | 1 byte | ~70 GB | Negligible (<0.1%) |
| **INT4 (4-bit)** | 4 bits | 0.5 bytes | ~35 GB | Minor (<1-2%) |

### Symmetric vs Asymmetric Quantization

Quantization scales floating-point weight values $W_{float}$ into integer bounds $[-128, 127]$ (INT8):

$$W_{quant} = \text{round}\left( \frac{W_{float}}{S} \right) + Z$$

Where $S$ is the scale factor and $Z$ is zero-point offset.

## Example

PyTorch scale factor calculation for symmetric INT8 quantization:

```python
import torch

def quantize_int8(w_float: torch.Tensor):
    max_val = torch.max(torch.abs(w_float))
    scale = max_val / 127.0
    w_int8 = torch.clamp(torch.round(w_float / scale), -128, 127).to(torch.int8)
    return w_int8, scale

weights = torch.tensor([-3.4, 0.0, 1.2, 5.8], dtype=torch.float32)
w_int8, scale = quantize_int8(weights)

print("Quantized INT8 weights:", w_int8)
print("Dequantized approximation:", w_int8.float() * scale)
```

## Interview tips

- Distinguish Post-Training Quantization (PTQ, e.g. AWQ, GPTQ, GGUF) from Quantization-Aware Training (QAT).
- Explain how 4-bit quantization (NF4 in QLoRA) allows fine-tuning 70B models on a single 48GB GPU.

---

[⬅ Back to Fine-Tuning and Adaptation](./README.md) · [All topics](../README.md)
