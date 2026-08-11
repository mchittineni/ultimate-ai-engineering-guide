---
title: "How does Active Prompting dynamically select the best exemplars for few-shot learning?"
id: 117
category: "Prompt Engineering"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - prompt-engineering
  - interview-questions
---

# How does Active Prompting dynamically select the best exemplars for few-shot learning?

**Short answer:** Active Prompting dynamically queries an LLM on candidate unlabeled task inputs, measures prediction uncertainty (via output variance or entropy across multiple sampled outputs), selects the highest-uncertainty items for human annotation, and appends them as few-shot exemplars.

## Detail

Static few-shot prompting uses fixed, hardcoded examples that may not assist the model on hard edge cases.

```
[Unlabeled Pool of Inputs] ──► [LLM Uncertainty Sampler] ──► Select High Uncertainty Items
                                                                        │
                                                                        ▼
[Dynamic Exemplar Store] ◄── Human Annotates Edge Case ◄────────── Annotate Items
```

### Active Prompting Step-by-Step Workflow

1. **Uncertainty Estimation:** Run candidate query $X$ through the LLM $K$ times (with $T > 0$) to generate $K$ predictions. Calculate output variance or entropy.
2. **Targeted Selection:** Rank queries by uncertainty score; identify inputs where prediction variance is highest.
3. **Annotated Exemplar Insertion:** Have domain experts annotate the most uncertain queries and add them to the few-shot prompt context window.

## Example

Python concept calculating output entropy across multiple LLM runs for exemplar selection:

```python
from collections import Counter
import math

def calculate_prediction_uncertainty(sample_outputs: list[str]) -> float:
    # Calculate Shannon Entropy across output predictions
    total = len(sample_outputs)
    counts = Counter(sample_outputs)
    entropy = 0.0
    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy # High entropy = high uncertainty

# Model generated 5 identical outputs -> Low uncertainty (0.0)
print("Uncertainty Low:", calculate_prediction_uncertainty(["Label A", "Label A", "Label A", "Label A", "Label A"]))
# Model generated split outputs -> High uncertainty
print("Uncertainty High:", calculate_prediction_uncertainty(["Label A", "Label B", "Label C", "Label A", "Label B"]))
```

## Interview tips

- Contrast Active Prompting with naive static few-shot prompting: Active Prompting spends annotation budget exclusively on model blind spots.
- Connect uncertainty sampling to Active Learning in traditional machine learning pipelines.

## Related Concepts

- [[How does Automatic Prompt Engineer (APE) optimize prompt selection using search?]] (`#118`): [How does Automatic Prompt Engineer (APE) optimize prompt selection using search?](../prompt-engineering/how-does-automatic-prompt-engineer-ape-optimize-prompt-selection-using-search.md)
- [[How to build a continuous evaluation pipeline sampling production traces for human review?]] (`#168`): [How to build a continuous evaluation pipeline sampling production traces for human review?](../llmops-and-production-ai/how-to-build-a-continuous-evaluation-pipeline-sampling-production-traces-for-human-review.md)
- [[What is human evaluation (RLHF human rating) and how do you design annotation rubrics?]] (`#175`): [What is human evaluation (RLHF human rating) and how do you design annotation rubrics?](../evaluation-and-testing/what-is-human-evaluation-rlhf-human-rating-and-how-do-you-design-annotation-rubrics.md)

---

[⬅ Back to Prompt Engineering](./README.md) · [All topics](../README.md)
