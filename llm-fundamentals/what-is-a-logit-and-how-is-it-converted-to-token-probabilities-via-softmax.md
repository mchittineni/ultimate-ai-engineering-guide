---
title: "What is a logit and how is it converted to token probabilities via Softmax?"
id: 103
category: "LLM Fundamentals"
difficulty: "Beginner"
tags:
  - ai-engineering
  - llm-fundamentals
  - interview-questions
---

# What is a logit and how is it converted to token probabilities via Softmax?

**Short answer:** A logit is an unnormalized floating-point prediction score emitted by the final linear projection layer of an LLM for each token in the vocabulary ($\mathbb{R}^{V}$); the Softmax function exponentiates and normalizes these raw logits into a valid probability distribution summing to 1.0.

## Detail

The final layer of a Transformer projects hidden states $h \in \mathbb{R}^{d}$ to vocabulary dimension $V$ via $z = h W_{vocab}$.

```
Hidden State h (4096-dim) ──► W_vocab Projection ──► Raw Logits z (128,000-dim)
                                                          │
                                                          ▼
                                                  Softmax Function
                                                          │
                                                          ▼
                                              Probabilities P (Sums to 1.0)
```

### Softmax Formula with Temperature Scaling

$$P_i = \frac{e^{z_i / T}}{\sum_{j=1}^{V} e^{z_j / T}}$$

Where $T$ is temperature:
- **Low Temperature ($T \to 0$):** Sharpens probability distribution toward the argmax logit (greedy sampling).
- **High Temperature ($T > 1.0$):** Flattens probability distribution, increasing output diversity.

## Example

PyTorch conversion of logits to probabilities with temperature scaling:

```python
import torch

logits = torch.tensor([2.0, 1.0, 0.1, -1.5])
temperature = 0.7

# Temperature-scaled Softmax
probs = torch.softmax(logits / temperature, dim=-1)

print("Raw Logits:", logits.tolist())
print("Token Probabilities:", [round(p, 4) for p in probs.tolist()])
print("Sum of Probabilities:", round(probs.sum().item(), 4))
```

## Interview tips

- Discuss numerical stability trick in Softmax: subtracting $\max(z)$ from logits before exponentiating ($e^{z_i - \max(z)}$) to prevent floating-point overflow.
- Connect logits to logit bias parameters in OpenAI/vLLM APIs.

## Related Concepts

- [[What is Temperature, Top-p, and Top-k sampling?]] (`#51`): [What is Temperature, Top-p, and Top-k sampling?](../llm-fundamentals/what-is-temperature-top-p-and-top-k-sampling.md)
- [[What is learning rate scheduling (cosine decay) during LLM fine-tuning?]] (`#142`): [What is learning rate scheduling (cosine decay) during LLM fine-tuning?](../fine-tuning-and-adaptation/what-is-learning-rate-scheduling-cosine-decay-during-llm-fine-tuning.md)
- [[What is SLA/SLO monitoring for Time-to-First-Token (TTFT) and throughput (Tokens/sec)?]] (`#163`): [What is SLA/SLO monitoring for Time-to-First-Token (TTFT) and throughput (Tokens/sec)?](../llmops-and-production-ai/what-is-sla-slo-monitoring-for-time-to-first-token-ttft-and-throughput-tokens-sec.md)

---

[⬅ Back to LLM Fundamentals](./README.md) · [All topics](../README.md)
