---
title: "How to measure model hallucination rate using NLI (Natural Language Inference) entailment models?"
id: 176
category: "Evaluation and Testing"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - evaluation-and-testing
  - interview-questions
---

# How to measure model hallucination rate using NLI (Natural Language Inference) entailment models?

**Short answer:** Measuring hallucination using Natural Language Inference (NLI) fine-tunes small classification models (e.g. DeBERTa-v3) to score whether generated output statements are logically entailed by (`Entailment`), neutral to (`Neutral`), or contradicted by (`Contradiction`) retrieved source context passages.

## Detail

LLM-as-a-Judge evaluations using GPT-4o are accurate but expensive for high-volume production monitoring.

NLI cross-encoder models evaluate hallucination deterministically at $100\times$ lower latency and cost.

```text
Premise (Retrieved Context): "Company revenue grew 15% in Q3 to $5M."
Hypothesis (LLM Output):    "Company revenue was $5M in Q3."
                                        │
                                        ▼
                  [DeBERTa NLI Cross-Encoder Classifier]
                                        │
                                        ▼
         Probabilities: [Entailment: 0.98, Neutral: 0.01, Contradiction: 0.01]
         ──► Status: GROUNDED (Zero Hallucination)
```

### NLI Classification Categories

- **Entailment ($P_{entail}$):** The premise logically proves the hypothesis is true.
- **Neutral ($P_{neutral}$):** The hypothesis introduces extra un-verifiable details not in the premise.
- **Contradiction ($P_{contra}$):** The hypothesis directly contradicts the premise (Hallucination!).

## Example

PyTorch Transformers NLI entailment evaluation snippet:

```python
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("cross-encoder/nli-deberta-v3-base")
model = AutoModelForSequenceClassification.from_pretrained("cross-encoder/nli-deberta-v3-base")

premise = "The refund policy permits returns within 14 days."
hypothesis = "Customers have 30 days to return items." # Contradiction!

inputs = tokenizer(premise, hypothesis, return_tensors="pt")
with torch.no_grad():
    logits = model(**inputs).logits
    probs = torch.softmax(logits, dim=-1)

# Labels: [0: contradiction, 1: entailment, 2: neutral]
print(f"Contradiction Probability: {probs[0][0].item():.4f}") # High contradiction -> Hallucination!
```

## Interview tips

- Highlight that NLI models provide fast, objective, reproducible hallucination scores without prompt engineering variability.
- Explain claim-level decomposition: splitting long LLM responses into atomic sentence claims before running NLI checks.

## Related Concepts

- [[How does Self-RAG train models to dynamically decide when to retrieve, evaluate, and critique documents?]] (`#130`): [How does Self-RAG train models to dynamically decide when to retrieve, evaluate, and critique documents?](../rag-and-vector-databases/how-does-self-rag-train-models-to-dynamically-decide-when-to-retrieve-evaluate-and-critique-documents.md)
- [[How to build an automated RAG evaluation harness measuring Context Precision and Recall?]] (`#178`): [How to build an automated RAG evaluation harness measuring Context Precision and Recall?](../evaluation-and-testing/how-to-build-an-automated-rag-evaluation-harness-measuring-context-precision-and-recall.md)

---

[⬅ Back to Evaluation and Testing](./README.md) · [All topics](../README.md)
