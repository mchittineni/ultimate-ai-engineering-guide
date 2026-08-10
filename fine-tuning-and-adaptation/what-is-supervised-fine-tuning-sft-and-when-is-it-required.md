---
title: "What is Supervised Fine-Tuning (SFT) and when is it required?"
id: 71
category: "Fine-Tuning and Adaptation"
difficulty: "Beginner"
tags:
  - ai-engineering
  - fine-tuning-and-adaptation
  - interview-questions
---

# What is Supervised Fine-Tuning (SFT) and when is it required?

**Short answer:** Supervised Fine-Tuning (SFT) trains a pre-trained base model on curated instruction-response dataset pairs using cross-entropy loss, adapting raw next-token completion models into conversational instruction-following assistants.

## Detail

Base foundation models (e.g. Llama-3-8B-Base) are trained on raw web corpora. When prompted with a question like _"How do I bake a cake?"_, a base model may complete the text by continuing with more questions rather than providing an answer.

```text
Base Model:        Prompt: "How to bake a cake?" ──► Completion: "How to bake bread? How to make pasta?"
SFT Instruct Model: Prompt: "How to bake a cake?" ──► Completion: "Step 1: Preheat oven to 350°F..."
```

### When SFT is Required

1. **Instruction Formatting:** Teaching base models to obey system prompts, user turns, and assistant completion roles.
2. **Domain Syntax / Tone Adaptation:** Enforcing specialized structured output syntax (e.g. specialized medical reporting formats, proprietary SQL dialects).
3. **Preference Pre-requisite:** SFT is required prior to applying preference alignment (DPO, RLHF, GRPO).

## Example

HuggingFace SFTTrainer configuration pattern:

```python
from trl import SFTTrainer
from transformers import TrainingArguments

training_args = TrainingArguments(
    output_dir="./sft_output",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-5,
    num_train_epochs=3,
    logging_steps=10,
    fp16=True
)

# SFTTrainer takes dataset formatted into instruction-response pairs
# trainer = SFTTrainer(model=model, args=training_args, train_dataset=dataset)
```

## Interview tips

- Contrast SFT with RAG: SFT teaches **style, tone, and format**, while RAG provides **dynamic external facts**.
- Emphasize dataset quality over quantity: 1,000 high-quality, verified instruction pairs often outperform 100,000 noisy scraped pairs (LIMA paper finding).

---

[⬅ Back to Fine-Tuning and Adaptation](./README.md) · [All topics](../README.md)
