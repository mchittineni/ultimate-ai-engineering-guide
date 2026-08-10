---
title: "What is the difference between greedy decoding and beam search?"
id: 52
category: "LLM Fundamentals"
difficulty: "Beginner"
tags:
  - ai-engineering
  - llm-fundamentals
  - interview-questions
---

# What is the difference between greedy decoding and beam search?

**Short answer:** Greedy decoding selects the highest probability single token at each step ($O(1)$ breadth); Beam search maintains $B$ candidate sequences (beams) in parallel, selecting the sequence with the highest cumulative log-probability over time.

## Detail

Autoregressive decoding generates text sequence $Y = (y_1, y_2, \dots, y_T)$ given prompt $X$:

$$\arg\max_Y P(Y|X) = \prod_{t=1}^T P(y_t | y_{<t}, X)$$

### Decoding Comparison

1. **Greedy Decoding:** Makes a locally optimal choice at step $t$. If an early token leads to poor global sequence probabilities later, greedy decoding cannot backtrack or recover.
2. **Beam Search:** Retains a beam width $B$ (e.g. $B=4$). At each step, it expands all $B$ paths into $B \times V$ candidates and keeps the top $B$ cumulative log-probability sequences:

$$\text{Score}(Y) = \frac{1}{T^\alpha} \sum_{t=1}^T \log P(y_t | y_{<t}, X)$$

Where $T^\alpha$ normalizes for sequence length to avoid favoring short completions.

| Metric                      | Greedy Decoding                            | Beam Search                                                |
| --------------------------- | ------------------------------------------ | ---------------------------------------------------------- |
| **Compute / Memory**        | Low (Single state pass)                    | High ($B \times$ forward passes & KV cache streams)        |
| **Primary Use Cases**       | Chat, code generation, real-time streaming | Translation, summarization, deterministic sequence parsing |
| **Streaming Compatibility** | High                                       | Low (Must evaluate full beams before outputting)           |

## Example

Python concept illustrating greedy vs beam candidate tracking:

```python
# Greedy decoding step
next_token = logits.argmax(dim=-1)

# Beam search step (B=2 candidate sequences)
top2_probs, top2_indices = torch.topk(torch.softmax(logits, dim=-1), k=2)
beams = [
    {"seq": [idx.item()], "score": torch.log(prob).item()}
    for prob, idx in zip(top2_probs[0], top2_indices[0])
]
print("Top 2 initial beams:", beams)
```

## Interview tips

- Note that beam search can produce repetitive text in long-form generation, which is why sampling ($T, p, k$) is preferred for chat models.
- Explain why beam search is incompatible with real-time token streaming UIs.

---

[⬅ Back to LLM Fundamentals](./README.md) · [All topics](../README.md)
