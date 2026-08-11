---
title: "What is dataset formatting for instruction tuning (Alpaca vs ShareGPT formats)?"
id: 141
category: "Fine-Tuning and Adaptation"
difficulty: "Beginner"
tags:
  - ai-engineering
  - fine-tuning-and-adaptation
  - interview-questions
---

# What is dataset formatting for instruction tuning (Alpaca vs ShareGPT formats)?

**Short answer:** Alpaca dataset format structures single-turn training items into `instruction`, `input`, and `output` key-value pairs; ShareGPT dataset format structures multi-turn dialogue histories into lists of `conversations` objects containing `from` and `value` fields.

## Detail

Supervised Fine-Tuning (SFT) requires datasets formatted into structured schemas compatible with training libraries (like HuggingFace TRL or LLaMA-Factory).

### 1. Alpaca Single-Turn Format

Designed for single-turn instruction-response tasks:

```json
{
  "instruction": "Summarize the customer complaint.",
  "input": "Order #123 arrived broken...",
  "output": "Customer received a damaged shipment for order #123."
}
```

### 2. ShareGPT Multi-Turn Format

Designed for complex multi-turn conversation logs:

```json
{
  "conversations": [
    {"from": "human", "value": "Write a SQL query to fetch total users."},
    {"from": "gpt", "value": "SELECT count(*) FROM users;"},
    {"from": "human", "value": "Now filter by active users only."}
  ]
}
```

## Example

Python dataset converter from Alpaca format to ShareGPT format:

```python
def convert_alpaca_to_sharegpt(alpaca_item: dict) -> dict:
    user_content = alpaca_item["instruction"]
    if alpaca_item.get("input"):
        user_content += f"\nContext:\n{alpaca_item['input']}"
        
    return {
        "conversations": [
            {"from": "human", "value": user_content},
            {"from": "gpt", "value": alpaca_item["output"]}
        ]
    }

alpaca_example = {
    "instruction": "Fix code bugs.",
    "input": "def add(a,b) return a+b",
    "output": "def add(a, b): return a + b"
}
print(convert_alpaca_to_sharegpt(alpaca_example))
```

## Interview tips

- Discuss loss masking in ShareGPT formatting: masking loss computation on `human` turns so the gradient updates calculate cross-entropy loss exclusively on `gpt` assistant responses.
- Connect dataset formats to ChatML system templates.

## Related Concepts

- [[What is weight merging in LoRA and why does it eliminate inference latency penalties?]] (`#145`): [What is weight merging in LoRA and why does it eliminate inference latency penalties?](../fine-tuning-and-adaptation/what-is-weight-merging-in-lora-and-why-does-it-eliminate-inference-latency-penalties.md)
- [[How does ORPO perform SFT and alignment in a single step without reference models?]] (`#149`): [How does ORPO perform SFT and alignment in a single step without reference models?](../fine-tuning-and-adaptation/how-does-orpo-perform-sft-and-alignment-in-a-single-step-without-reference-models.md)
- [[How to answer scenario questions about trade-offs between RAG and Fine-Tuning?]] (`#194`): [How to answer scenario questions about trade-offs between RAG and Fine-Tuning?](../interview-experience/how-to-answer-scenario-questions-about-trade-offs-between-rag-and-fine-tuning.md)

---

[⬅ Back to Fine-Tuning and Adaptation](./README.md) · [All topics](../README.md)
