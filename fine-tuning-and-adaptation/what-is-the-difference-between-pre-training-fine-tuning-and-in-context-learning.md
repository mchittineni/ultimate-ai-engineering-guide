---
title: "What is the difference between pre-training, fine-tuning, and in-context learning?"
id: 27
category: "Fine-Tuning and Adaptation"
difficulty: "Beginner"
tags:
  - ai-engineering
  - fine-tuning-and-adaptation
  - interview-questions
---

# What is the difference between pre-training, fine-tuning, and in-context learning?

**Short answer:** Pre-training builds foundational language understanding by updating all model weights on trillions of tokens via unsupervised next-token prediction; fine-tuning updates model weights on task-specific dataset pairs to adapt behavior; in-context learning (RAG & prompting) adapts model output at inference time using context window instructions without modifying any model weights.

## Detail

Model adaptation strategies trade off compute cost, dataset requirements, and update latency:

| Dimension | Pre-Training | Fine-Tuning (Full / PEFT) | In-Context Learning (Prompt/RAG) |
| --- | --- | --- | --- |
| **Weight Modification** | Updates 100% of parameters | Updates 100% (Full) or <1% (LoRA) | 0% (Weights frozen) |
| **Compute / GPU Cost** | Millions of USD (Thousands of H100 GPUs) | Hundreds of USD (Single/Few GPUs) | API invocation token cost |
| **Data Requirement** | Trillions of tokens | Hundreds to thousands of curated pairs | 1 to 20 context documents |
| **Knowledge Update** | Permanent baseline knowledge | Adaptation of tone, format, domain style | Real-time / Dynamic facts |
| **Latency Impact** | N/A | None (Same architecture inference) | Higher latency due to prompt token overhead |

## Example

Conceptual Python distinction:

```python
# 1. In-Context Learning: Prompt contains instruction + data (No weight changes)
icl_prompt = "Translate to French:\nEnglish: Hello\nFrench:"

# 2. Fine-Tuning (LoRA / HuggingFace Trainer): Updates adapter weight matrix
# trainer.train() updates model parameters based on task loss loss.backward()
```

## Interview tips

- Emphasize the core rule of thumb: Use RAG/In-Context Learning to provide **knowledge and dynamic facts**; use Fine-Tuning to teach **format, style, tone, and domain syntax**.
- Mention PEFT/LoRA as the modern standard for cost-effective fine-tuning.

---

[⬅ Back to Fine-Tuning and Adaptation](./README.md) · [All topics](../README.md)
