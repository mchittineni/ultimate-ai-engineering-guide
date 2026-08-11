---
title: "What is mixed precision training (FP16 vs BF16) and why is BF16 preferred on modern GPUs?"
id: 144
category: "Fine-Tuning and Adaptation"
difficulty: "Beginner"
tags:
  - ai-engineering
  - fine-tuning-and-adaptation
  - interview-questions
---

# What is mixed precision training (FP16 vs BF16) and why is BF16 preferred on modern GPUs?

**Short answer:** Mixed precision training executes matrix multiplications in 16-bit precision while storing master weights in 32-bit (FP32) to halve memory and double GPU Tensor Core speed; BF16 (Bfloat16) is preferred over FP16 because it preserves the exact dynamic range exponent scale as FP32, eliminating FP16 numerical underflow/overflow crashes.

## Detail

Standard single precision (FP32) uses 32 bits (1 sign, 8 exponent, 23 mantissa).

```text
FP32 (32-bit):     [Sign: 1] [Exponent: 8 bits] [Mantissa: 23 bits]  -> Dynamic Range ~10^38
FP16 (16-bit):     [Sign: 1] [Exponent: 5 bits] [Mantissa: 10 bits]  -> Dynamic Range ~65,504 (Prone to Overflow!)
BF16 (Bfloat16):   [Sign: 1] [Exponent: 8 bits] [Mantissa: 7 bits]   -> Dynamic Range ~10^38 (Same Range as FP32!)
```

### Why FP16 Requires Loss Scaling

FP16's 5-bit exponent limits max values to $65,504$. Small gradient values ($< 6 \times 10^{-5}$) underflow to zero, requiring dynamic loss scaling ($L_{scaled} = L \times S$) to prevent gradient death.

BF16 retains FP32's 8-bit exponent, providing identical dynamic range ($\sim 10^{38}$) without needing loss scaling.

| Precision Format | Bits | Dynamic Range               | Underflow Risk              | Hardware Requirement       |
| ---------------- | ---- | --------------------------- | --------------------------- | -------------------------- |
| **FP32**         | 32   | $10^{-38} - 10^{38}$        | Minimal                     | All GPUs                   |
| **FP16**         | 16   | $6 \times 10^{-5} - 65,504$ | High (Requires Loss Scaler) | NVIDIA Volta (V100)+       |
| **BF16**         | 16   | $10^{-38} - 10^{38}$        | Minimal (No Loss Scaler)    | NVIDIA Ampere (A100/H100)+ |

## Example

PyTorch `torch.cuda.amp` mixed-precision context with BF16:

```python
import torch

model = torch.nn.Linear(100, 100).cuda()
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
x = torch.randn(32, 100).cuda()

# Automatic Mixed Precision (AMP) using Bfloat16
with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
    output = model(x)
    loss = output.sum()

loss.backward()
optimizer.step()
print("Forward/Backward executed in BF16 mixed precision.")
```

## Interview tips

- Explain that NVIDIA Ampere (A100), Hopper (H100), and Blackwell (B200) natively support BF16 Tensor Cores.
- Highlight that BF16 reduces VRAM weight footprint by $50\%$ compared to FP32.

## Related Concepts

- [[What is gradient accumulation and how does it simulate larger batch sizes on small GPUs?]] (`#143`): [What is gradient accumulation and how does it simulate larger batch sizes on small GPUs?](../fine-tuning-and-adaptation/what-is-gradient-accumulation-and-how-does-it-simulate-larger-batch-sizes-on-small-gpus.md)
- [[How does GGUF format enable quantization and CPU/GPU offloading in llama.cpp?]] (`#147`): [How does GGUF format enable quantization and CPU/GPU offloading in llama.cpp?](../fine-tuning-and-adaptation/how-does-gguf-format-enable-quantization-and-cpu-gpu-offloading-in-llama-cpp.md)

---

[⬅ Back to Fine-Tuning and Adaptation](./README.md) · [All topics](../README.md)
