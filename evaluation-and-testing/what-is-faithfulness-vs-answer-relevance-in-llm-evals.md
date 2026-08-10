---
title: "What is faithfulness vs answer relevance in LLM evals?"
id: 87
category: "Evaluation and Testing"
difficulty: "Beginner"
tags:
  - ai-engineering
  - evaluation-and-testing
  - interview-questions
---

# What is faithfulness vs answer relevance in LLM evals?

**Short answer:** Faithfulness measures whether the LLM's generated response is strictly grounded in the retrieved context snippets (measuring hallucination); Answer Relevance measures whether the generated response directly addresses the user's prompt (measuring completeness and helpfulness).

## Detail

Evaluating generation quality in RAG applications requires evaluating two distinct failure modes:

```
                  ┌──► Faithfulness Score  ──► "Is the answer 100% grounded in context?"
[Generated Answer]┤                            (Detects hallucinations / fabricated facts)
                  └──► Answer Relevance    ──► "Does the answer directly address the prompt?"
                                               (Detects evasive or off-topic responses)
```

| Metric | High Score Meaning | Failure Mode Identified |
| --- | --- | --- |
| **Faithfulness** | Every claim in the output is supported by retrieved context. | Hallucination / Claim Fabrication |
| **Answer Relevance** | Response directly addresses the user's query without fluff. | Off-topic rambling / Evasive answers |

### Faithfulness Calculation

$$\text{Faithfulness Score} = \frac{\text{Number of Claims in Answer Grounded in Context}}{\text{Total Claims Made in Answer}}$$

## Example

Python concept evaluating faithfulness using claim decomposition:

```python
def evaluate_faithfulness(claims_in_answer: list[str], retrieved_context: str) -> float:
    grounded_claims = 0
    for claim in claims_in_answer:
        # Check if claim is directly supported by retrieved context
        if claim in retrieved_context:
            grounded_claims += 1
    return grounded_claims / len(claims_in_answer) if claims_in_answer else 0.0

claims = ["Database updated successfully", "Server uptime is 99.9%"]
context = "Database updated successfully at 10:00 AM."
print("Faithfulness Score:", evaluate_faithfulness(claims, context)) # 0.5 (1 claim ungrounded)
```

## Interview tips

- Highlight that an answer can be 100% Faithful (fully grounded in context) but 0% Relevant (if the retrieved context was completely off-topic).
- Explain using LLM-as-a-Judge to decompose outputs into atomic claims for scoring.

---

[⬅ Back to Evaluation and Testing](./README.md) · [All topics](../README.md)
