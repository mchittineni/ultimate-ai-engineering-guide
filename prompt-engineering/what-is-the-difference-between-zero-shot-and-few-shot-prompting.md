---
title: "What is the difference between zero-shot and few-shot prompting?"
id: 15
category: "Prompt Engineering"
difficulty: "Beginner"
tags:
  - ai-engineering
  - prompt-engineering
  - interview-questions
---

# What is the difference between zero-shot and few-shot prompting?

**Short answer:** Zero-shot prompting evaluates an LLM on a task without giving any input-output examples, relying entirely on pre-trained knowledge; few-shot prompting provides one or more demonstrative input-output pairs within the prompt context to ground the expected format, style, or reasoning pattern.

## Detail

In-context learning (ICL) enables LLMs to adapt to specific tasks without weight updates.

| Aspect | Zero-Shot Prompting | Few-Shot Prompting |
| --- | --- | --- |
| **Examples Provided** | 0 examples | 1 to $N$ examples (typically 3–5) |
| **Context Window Overhead** | Minimal | Higher (depends on example token count) |
| **Format Consistency** | Can drift or vary | Highly consistent format adherence |
| **Best Used For** | Standard knowledge queries & instructions | Complex formatting, edge cases, domain taxonomies |

### Key Guidelines for Few-Shot Examples

1. **Diversity:** Cover edge cases and common variations.
2. **Label Balance:** Avoid biasing the model by ensuring exemplar labels are balanced across output classes.
3. **Format Alignment:** Match the exact structure required in the final output (e.g., JSON schemas).

## Example

```python
# Zero-Shot Prompt
zero_shot = "Classify text sentiment: 'The API latency is terrible today.' ->"

# Few-Shot Prompt
few_shot = """Classify text sentiment into [Positive, Negative, Neutral].

Text: "The system uptime was 99.99% this quarter."
Sentiment: Positive

Text: "The API latency is terrible today."
Sentiment: Negative

Text: "The server restarted at 02:00 UTC."
Sentiment: Neutral

Text: "Deployment succeeded with zero errors."
Sentiment:"""
```

## Interview tips

- Highlight that few-shot examples consume context tokens, introducing cost and latency trade-offs.
- Mention that noisy or mislabeled few-shot examples can significantly degrade generation accuracy.

---

[⬅ Back to Prompt Engineering](./README.md) · [All topics](../README.md)
