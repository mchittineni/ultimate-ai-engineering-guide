---
title: "What is LoRA and QLoRA for efficient fine-tuning?"
id: 6
category: "Fine-Tuning and Adaptation"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - fine-tuning-and-adaptation
  - interview-questions
---

# What is LoRA and QLoRA for efficient fine-tuning?

**Short answer:** Low-Rank Adaptation (LoRA) decomposes weight update matrices into two low-rank matrices to fine-tune LLMs with >99% fewer trainable parameters, while QLoRA quantizes the base model to 4-bit NormalFloat (NF4) memory precision to enable fine-tuning 70B models on a single GPU.

## Detail

Full Parameter Fine-Tuning requires updating and storing gradients, optimizer states (AdamW requires 8 bytes per parameter), and activations for all billions of parameters. Fine-tuning Llama-3-70B fully requires over 1.2 TB of VRAM across massive GPU clusters.

### LoRA (Low-Rank Adaptation)

LoRA freezes the pre-trained model weights $W_0 \in \mathbb{R}^{d \times k}$ and injects trainable rank decomposition matrices:

$$W = W_0 + \Delta W = W_0 + B \cdot A$$

where $B \in \mathbb{R}^{d \times r}$ and $A \in \mathbb{R}^{r \times k}$, with rank $r \ll \min(d, k)$ (typically $r \in [8, 64]$).

- Matrix $A$ is initialized with a Gaussian distribution, and $B$ is initialized to 0 (ensuring $\Delta W = 0$ at start).
- Scaled by factor $\frac{\alpha}{r}$: $W = W_0 + \frac{\alpha}{r} (B A)$.
- **Zero Inference Latency:** At deployment, $B \cdot A$ can be permanently merged back into $W_0$, adding zero latency overhead.

### QLoRA (Quantized Low-Rank Adaptation)

QLoRA enhances LoRA memory efficiency with three breakthroughs:

1. **4-bit NormalFloat (NF4):** An information-theoretically optimal quantile quantization data type for normally distributed neural network weights.
2. **Double Quantization (DQ):** Quantizes the quantization constants themselves, saving an additional 0.37 bits per parameter.
3. **Paged Optimizers:** Uses CUDA Unified Memory to automatically page optimizer state spikes to CPU RAM during long sequence gradient steps.

```text
Full Precision Fine-Tuning    LoRA (FP16 Base)              QLoRA (NF4 4-bit Base)
┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────────┐
│  Trainable Base      │    │  Frozen FP16 Base    │    │  Frozen 4-bit NF4    │
│  Weights (70B)       │    │  Weights (70B)       │    │  Base Weights (70B)  │
│  + FP32 Gradients    │    │  + Trainable Low-    │    │  + Trainable FP16    │
│  + FP32 Optimizer    │    │    Rank Adapters     │    │    LoRA Adapters     │
└──────────────────────┘    └──────────────────────┘    └──────────────────────┘
     VRAM: ~1,200 GB             VRAM: ~160 GB               VRAM: ~48 GB
```

## Example

Configuring QLoRA in PyTorch using Hugging Face `peft` and `bitsandbytes`:

```python
import torch
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# 1. Configure 4-bit Quantization (QLoRA)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True
)

# 2. Load Base Model in 4-bit
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Meta-Llama-3-8B",
    quantization_config=bnb_config,
    device_map="auto"
)
model = prepare_model_for_kbit_training(model)

# 3. Configure LoRA Adapter
peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, peft_config)
model.print_trainable_parameters()
# Outputs: trainable params: 13,631,488 || all params: 8,043,892,736 || trainable%: 0.169%
```

## Interview tips

- Understand the relationship between rank $r$ and scaling factor $\alpha$: $\alpha$ controls the learning rate multiplier for adapter updates. Setting $\alpha = 2r$ is a common empirical default.
- Know which modules to target: targeting all linear projections (`q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`) yields better task adaptation than targeting attention projections alone.

---

[⬅ Back to Fine-Tuning and Adaptation](./README.md) · [All topics](../README.md)
