---
title: "What is GPU VRAM bandwidth and why is decoding memory-bound?"
id: 78
category: "AI System Design"
difficulty: "Beginner"
tags:
  - ai-engineering
  - ai-system-design
  - interview-questions
---

# What is GPU VRAM bandwidth and why is decoding memory-bound?

**Short answer:** GPU VRAM memory bandwidth measures the speed at which data transfers from High Bandwidth Memory (HBM) into processing SRAM; autoregressive token decoding is memory-bandwidth bound because every single generated token requires transferring the entire multi-gigabyte model weight matrix through the memory bus for just 1 token of compute.

## Detail

The Arithmetic Intensity of an algorithm is defined as:

$$\text{Arithmetic Intensity} = \frac{\text{Total Floating-Point Operations (FLOPs)}}{\text{Total Memory Bytes Transferred}}$$

### Why Decoding Has Low Arithmetic Intensity

Consider generating 1 token on a batch size of 1 using a 70B parameter model in FP16 precision:
- **Memory Transfer:** Transmitting 70B parameters $\times 2\text{ bytes} = 140\text{ GB}$ from GPU HBM to SRAM.
- **Compute Operations:** ~140 GigaFLOPs of tensor calculations.
- **Arithmetic Intensity:** $\frac{140 \times 10^9 \text{ FLOPs}}{140 \times 10^9 \text{ Bytes}} = 1 \text{ FLOP/Byte}$.

NVIDIA H100 GPUs provide 2,000 TFLOPs of compute but only 3.35 TB/s of memory bandwidth. At 1 FLOP/Byte intensity, the GPU compute cores spend $>95\%$ of their time waiting for HBM memory transfers to complete.

```
Roofline Model:
Decoding (Batch=1) ──► Low FLOP/Byte ──► Bound by HBM Bandwidth (~3.35 TB/s)
Prefill (Batch=N)  ──► High FLOP/Byte ──► Bound by Tensor Core FLOPs (~2000 TFLOPs)
```

## Example

Python calculation of theoretical maximum generation speed bound by HBM bandwidth:

```function
def theoretical_max_tokens_per_sec(model_params_billions: float, hbm_bandwidth_tb_s: float, precision_bytes: int = 2) -> float:
    vram_per_pass_gb = model_params_billions * precision_bytes
    hbm_bandwidth_gb_s = hbm_bandwidth_tb_s * 1000.0
    return hbm_bandwidth_gb_s / vram_per_pass_gb

# H100 GPU (3.35 TB/s) running 70B FP16 (140 GB per pass)
tok_per_sec = theoretical_max_tokens_per_sec(70, 3.35, precision_bytes=2)
print(f"Max single-stream decoding speed: {tok_per_sec:.1f} tokens/sec")
```

## Interview tips

- Explain how increasing batch size (continuous batching) or model quantization (INT4) improves arithmetic intensity and decoding throughput.
- Connect memory bandwidth constraints to speculative decoding.

---

[⬅ Back to AI System Design](./README.md) · [All topics](../README.md)
