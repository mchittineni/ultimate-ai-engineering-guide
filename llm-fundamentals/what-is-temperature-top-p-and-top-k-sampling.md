---
title: "What is Temperature, Top-p, and Top-k sampling?"
id: 51
category: "LLM Fundamentals"
difficulty: "Beginner"
tags:
  - ai-engineering
  - llm-fundamentals
  - interview-questions
---

# What is Temperature, Top-p, and Top-k sampling?

**Short answer:** Temperature scales raw logit values to control generation randomness; Top-k restricts token selection to the $k$ most probable tokens; Top-p (nucleus sampling) dynamic cuts off selection to the smallest set of cumulative probability tokens exceeding threshold $p$.

## Detail

LLM output generation converts raw unnormalized logit vectors into probability distributions over the vocabulary via Softmax:

$$P(w_i) = \frac{\exp(z_i / T)}{\sum_{j} \exp(z_j / T)}$$

| Parameter | Function | Value Range | Effect of Lower Value | Effect of Higher Value |
| --- | --- | --- | --- | --- |
| **Temperature ($T$)** | Divides logits before Softmax | $0.0 - 2.0$ | Deterministic, repetitive, focused ($T \to 0$ equals greedy decoding) | Creative, chaotic, random |
| **Top-$k$** | Keeps top $k$ highest logit tokens | $1 - N$ | Cuts off low probability tail strictly | Includes broader vocabulary tokens |
| **Top-$p$ (Nucleus)** | Truncates cumulative probability | $0.0 - 1.0$ | Restricts candidates dynamically based on distribution steepness | Expands candidate set |

## Example

PyTorch implementation of Top-$p$ (Nucleus) sampling filter:

```python
import torch

def top_p_sampling(logits: torch.Tensor, top_p: float = 0.9, temp: float = 0.7) -> torch.Tensor:
    logits = logits / temp
    sorted_logits, sorted_indices = torch.sort(logits, descending=True)
    cumulative_probs = torch.cumsum(torch.softmax(sorted_logits, dim=-1), dim=-1)

    # Remove tokens with cumulative probability above top_p threshold
    sorted_indices_to_remove = cumulative_probs > top_p
    sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
    sorted_indices_to_remove[..., 0] = 0

    indices_to_remove = sorted_indices_to_remove.scatter(0, sorted_indices, sorted_indices_to_remove)
    logits[indices_to_remove] = float('-inf')
    return torch.multinomial(torch.softmax(logits, dim=-1), num_samples=1)
```

## Interview tips

- Highlight that for factual Q&A or JSON code generation, $T=0.0$ or $T=0.2$ is preferred, whereas creative brainstorming uses $T=0.7 - 0.9$.
- Emphasize combining Top-$p$ and Temperature for balanced, non-repetitive responses.

---

[⬅ Back to LLM Fundamentals](./README.md) · [All topics](../README.md)
