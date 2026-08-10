---
title: "What is catastrophic forgetting during LLM fine-tuning?"
id: 72
category: "Fine-Tuning and Adaptation"
difficulty: "Beginner"
tags:
  - ai-engineering
  - fine-tuning-and-adaptation
  - interview-questions
---

# What is catastrophic forgetting during LLM fine-tuning?

**Short answer:** Catastrophic forgetting occurs when fine-tuning an LLM on a narrow domain dataset overwrites or degrades its pre-trained general knowledge, reasoning capabilities, or instruction-following skills.

## Detail

Full parameter fine-tuning updates all model weight matrices ($W$). Over multiple training epochs on specialized data (e.g. medical code translation), gradient updates displace weights essential for broader tasks (e.g. general math or logical reasoning).

```text
Base Model:      [General Reasoning + Coding + Math + Conversational Abilities]
Narrow Fine-tune: [Medical Translation Optimized] ──► (Loses Math & Coding accuracy)
```

### Mitigation Strategies

1. **Parameter-Efficient Fine-Tuning (PEFT / LoRA):** Freeze base model weights $W$ and train low-rank adapter matrices $A$ and $B$. This **reduces** forgetting; it does not eliminate it. The stored weights are untouched, but inference uses $W_0 + BA$, so the effective function still changes and general-capability scores can still regress. Adapters also give you a cheap escape hatch: unload the adapter and the base behaviour returns exactly.
2. **Data Replay / Mixing:** Mix 10–20% general pre-training or instruction data into the specialized domain dataset during SFT.
3. **Weight Averaging / Mergekit:** Interpolate fine-tuned weights back with base model weights (e.g. SLERP / Model Soups).

## Example

PyTorch LoRA adapter configuration freezing base parameters to limit catastrophic forgetting:

```python
from peft import LoraConfig, get_peft_model

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# get_peft_model freezes 99%+ of base parameters
# peft_model = get_peft_model(base_model, lora_config)
```

## Interview tips

- Say "reduces", not "prevents". LoRA constrains the update to a low-rank subspace and leaves the stored weights intact, which limits the damage — but a high rank, an aggressive learning rate, or many epochs on narrow data still degrades general capability. Claiming LoRA makes forgetting impossible is a trap; the honest answer is that it bounds and reverses it cheaply.
- Discuss testing fine-tuned models against standard benchmark suites (MMLU, HumanEval) to detect degradation — measuring it is the only way to know, which is itself the reason not to assert immunity.

---

[⬅ Back to Fine-Tuning and Adaptation](./README.md) · [All topics](../README.md)
