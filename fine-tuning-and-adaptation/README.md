---
title: "Fine-Tuning and Adaptation"
category: "Fine-Tuning and Adaptation"
tags:
  - ai-engineering
  - fine-tuning-and-adaptation
  - index
---

# Fine-Tuning and Adaptation

PEFT, LoRA, QLoRA, RLHF, DPO, GRPO, quantization (GGUF, AWQ, GPTQ), model distillation, and domain adaptation.

**20 questions** · 🟢 Beginner: 10 · 🟡 Intermediate: 6 · 🔴 Advanced: 4

## Questions

| # | Question | Difficulty |
| --- | --- | --- |
| 6 | [What is LoRA and QLoRA for efficient fine-tuning?](./what-is-lora-and-qlora-for-efficient-fine-tuning.md) | 🟡 Intermediate |
| 27 | [What is the difference between pre-training, fine-tuning, and in-context learning?](./what-is-the-difference-between-pre-training-fine-tuning-and-in-context-learning.md) | 🟢 Beginner |
| 28 | [What is quantization and how do INT8 and INT4 reduce LLM footprint?](./what-is-quantization-and-how-do-int8-and-int4-reduce-llm-footprint.md) | 🟢 Beginner |
| 29 | [How does Direct Preference Optimization (DPO) differ from RLHF?](./how-does-direct-preference-optimization-dpo-differ-from-rlhf.md) | 🟡 Intermediate |
| 30 | [How does Group Relative Policy Optimization (GRPO) work in DeepSeek R1?](./how-does-group-relative-policy-optimization-grpo-work-in-deepseek-r1.md) | 🔴 Advanced |
| 71 | [What is Supervised Fine-Tuning (SFT) and when is it required?](./what-is-supervised-fine-tuning-sft-and-when-is-it-required.md) | 🟢 Beginner |
| 72 | [What is catastrophic forgetting during LLM fine-tuning?](./what-is-catastrophic-forgetting-during-llm-fine-tuning.md) | 🟢 Beginner |
| 73 | [What is LoRA rank r and alpha scaling factor?](./what-is-lora-rank-r-and-alpha-scaling-factor.md) | 🟢 Beginner |
| 74 | [How does model distillation transfer knowledge from teacher to student?](./how-does-model-distillation-transfer-knowledge-from-teacher-to-student.md) | 🟡 Intermediate |
| 75 | [How does Kahneman-Tversky Optimization (KTO) differ from DPO?](./how-does-kahneman-tversky-optimization-kto-differ-from-dpo.md) | 🔴 Advanced |
| 141 | [What is dataset formatting for instruction tuning (Alpaca vs ShareGPT formats)?](./what-is-dataset-formatting-for-instruction-tuning-alpaca-vs-sharegpt-formats.md) | 🟢 Beginner |
| 142 | [What is learning rate scheduling (cosine decay) during LLM fine-tuning?](./what-is-learning-rate-scheduling-cosine-decay-during-llm-fine-tuning.md) | 🟢 Beginner |
| 143 | [What is gradient accumulation and how does it simulate larger batch sizes on small GPUs?](./what-is-gradient-accumulation-and-how-does-it-simulate-larger-batch-sizes-on-small-gpus.md) | 🟢 Beginner |
| 144 | [What is mixed precision training (FP16 vs BF16) and why is BF16 preferred on modern GPUs?](./what-is-mixed-precision-training-fp16-vs-bf16-and-why-is-bf16-preferred-on-modern-gpus.md) | 🟢 Beginner |
| 145 | [What is weight merging in LoRA and why does it eliminate inference latency penalties?](./what-is-weight-merging-in-lora-and-why-does-it-eliminate-inference-latency-penalties.md) | 🟢 Beginner |
| 146 | [How does DoRA (Weight-Decomposed Low-Rank Adaptation) improve directional weight updates over LoRA?](./how-does-dora-weight-decomposed-low-rank-adaptation-improve-directional-weight-updates-over-lora.md) | 🟡 Intermediate |
| 147 | [How does GGUF format enable quantization and CPU/GPU offloading in llama.cpp?](./how-does-gguf-format-enable-quantization-and-cpu-gpu-offloading-in-llama-cpp.md) | 🟡 Intermediate |
| 148 | [How does AWQ (Activation-aware Weight Quantization) preserve critical weights compared to GPTQ?](./how-does-awq-activation-aware-weight-quantization-preserve-critical-weights-compared-to-gptq.md) | 🟡 Intermediate |
| 149 | [How does ORPO perform SFT and alignment in a single step without reference models?](./how-does-orpo-perform-sft-and-alignment-in-a-single-step-without-reference-models.md) | 🔴 Advanced |
| 150 | [How does DeepSpeed ZeRO stage 1, 2, and 3 partition optimizer states, gradients, and parameters?](./how-does-deepspeed-zero-stage-1-2-and-3-partition-optimizer-states-gradients-and-parameters.md) | 🔴 Advanced |

## What interviewers probe here

- LoRA rank r and alpha scaling factor tuning.
- Preference optimization: RLHF vs DPO vs GRPO.
- Quantization techniques: INT8/INT4 weight-only vs KV cache quantization.

---

[⬅ Back to all topics](../README.md)
