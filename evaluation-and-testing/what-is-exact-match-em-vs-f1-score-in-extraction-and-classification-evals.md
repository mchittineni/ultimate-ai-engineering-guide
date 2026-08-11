---
title: "What is exact match (EM) vs F1 score in extraction and classification evals?"
id: 171
category: "Evaluation and Testing"
difficulty: "Beginner"
tags:
  - ai-engineering
  - evaluation-and-testing
  - interview-questions
---

# What is exact match (EM) vs F1 score in extraction and classification evals?

**Short answer:** Exact Match (EM) is a binary metric requiring generated outputs to match ground-truth reference strings character-for-character (1.0 or 0.0); F1 Score calculates the harmonic mean of token-level precision and recall, rewarding partial text matches and extraction completeness.

## Detail

Evaluating structured entity extraction or short-answer Q&A requires metrics that handle minor string variations.

```text
Ground Truth Answer: "San Francisco, California"
Generated Output:   "San Francisco, CA"

Exact Match (EM):  0.0 (String mismatch)
Token-level F1:    0.67 (Partial credit for matching "San" and "Francisco")
```

### Formulas

1. **Exact Match (EM):**

   $$\text{EM} = \begin{cases} 1.0 & \text{if } \text{normalize}(y_{pred}) == \text{normalize}(y_{true}) \\ 0.0 & \text{otherwise} \end{cases}$$

2. **Token-Level F1 Score:**

   $$\text{Precision} = \frac{|T_{pred} \cap T_{true}|}{|T_{pred}|}, \quad \text{Recall} = \frac{|T_{pred} \cap T_{true}|}{|T_{true}|}$$

   $$F_1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

## Example

Python implementation of EM and token-level F1 score:

```python
def calculate_em_and_f1(prediction: str, ground_truth: str) -> tuple[float, float]:
    pred_tokens = prediction.lower().split()
    gt_tokens = ground_truth.lower().split()

    # Exact Match
    em = 1.0 if prediction.strip().lower() == ground_truth.strip().lower() else 0.0

    # Token-level F1
    common = set(pred_tokens) & set(gt_tokens)
    if not common:
        return em, 0.0

    precision = len(common) / len(pred_tokens)
    recall = len(common) / len(gt_tokens)
    f1 = 2 * (precision * recall) / (precision + recall)
    return em, round(f1, 4)

print("Metrics:", calculate_em_and_f1("San Francisco, CA", "San Francisco, California"))
```

## Interview tips

- Emphasize text normalization (lowercasing, removing punctuation, stripping extra whitespace) prior to calculating EM and F1 scores.
- Discuss when EM is required (e.g. SQL query output or API key extraction) vs F1 (free-text summary extraction).

## Related Concepts

- [[What is BLEU and ROUGE scoring and why are they inadequate for modern LLM evaluation?]] (`#172`): [What is BLEU and ROUGE scoring and why are they inadequate for modern LLM evaluation?](../evaluation-and-testing/what-is-bleu-and-rouge-scoring-and-why-are-they-inadequate-for-modern-llm-evaluation.md)
- [[What is assertion testing in LLM unit tests?]] (`#173`): [What is assertion testing in LLM unit tests?](../evaluation-and-testing/what-is-assertion-testing-in-llm-unit-tests.md)
- [[How to build an automated RAG evaluation harness measuring Context Precision and Recall?]] (`#178`): [How to build an automated RAG evaluation harness measuring Context Precision and Recall?](../evaluation-and-testing/how-to-build-an-automated-rag-evaluation-harness-measuring-context-precision-and-recall.md)

---

[⬅ Back to Evaluation and Testing](./README.md) · [All topics](../README.md)
