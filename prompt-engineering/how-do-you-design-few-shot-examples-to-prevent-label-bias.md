---
title: "How do you design few-shot examples to prevent label bias?"
id: 59
category: "Prompt Engineering"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - prompt-engineering
  - interview-questions
---

# How do you design few-shot examples to prevent label bias?

**Short answer:** Label bias in few-shot prompting occurs when an unbalanced proportion or order of target labels in exemplars causes the model to favor specific outputs; it is mitigated by balancing class representations, randomizing exemplar ordering, and maintaining uniform length across examples.

## Detail

In-context learning is sensitive to example selection:

### Key Causes of Few-Shot Bias

1. **Majority Class Bias:** If 4 out of 5 exemplars demonstrate `"Positive"` sentiment, the model disproportionately predicts `"Positive"` for ambiguous inputs.
2. **Recency Bias:** The model tends to repeat the label shown in the final exemplar ($N$-th example) right before the user prompt.
3. **Format Asymmetry:** Detailed explanations in some exemplars and brief answers in others cause inconsistent output generation depth.

```text
Biased Exemplars:   [Doc1 -> Positive], [Doc2 -> Positive], [Doc3 -> Positive] (Biases prediction to Positive)
Balanced Exemplars: [Doc1 -> Positive], [Doc2 -> Negative], [Doc3 -> Neutral]  (Unbiased decision boundary)
```

## Example

Python helper to construct balanced few-shot prompts:

```python
from collections import Counter

def format_balanced_few_shot(examples: list[dict], target_query: str) -> str:
    # Verify label distribution balance
    labels = [ex["label"] for ex in examples]
    counts = Counter(labels)
    print("Label distribution in exemplars:", counts)

    formatted = "Classify customer feedback into [Bug, Feature Request, Question].\n\n"
    for ex in examples:
        formatted += f"Text: \"{ex['text']}\"\nCategory: {ex['label']}\n\n"

    formatted += f"Text: \"{target_query}\"\nCategory:"
    return formatted
```

## Interview tips

- Discuss how permutation of example order can alter accuracy by up to 20-30% on sensitive classification tasks.
- Mention using vector search to select dynamically relevant few-shot exemplars (k-NN exemplar selection) for each incoming user query.

---

[⬅ Back to Prompt Engineering](./README.md) · [All topics](../README.md)
