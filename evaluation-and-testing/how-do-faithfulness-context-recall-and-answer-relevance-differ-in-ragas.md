---
title: "How do Faithfulness, Context Recall, and Answer Relevance differ in Ragas?"
id: 9
category: "Evaluation and Testing"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - evaluation-and-testing
  - interview-questions
---

# How do Faithfulness, Context Recall, and Answer Relevance differ in Ragas?

**Short answer:** Ragas evaluates RAG systems by separating retrieval quality from generation quality: **Faithfulness** measures if the generated answer relies _only_ on retrieved context, **Answer Relevance** measures if the generated answer directly addresses the prompt, and **Context Recall** measures if the retriever fetched all ground-truth facts needed.

## Detail

Evaluating Retrieval-Augmented Generation (RAG) systems without ground-truth human annotations requires breaking down performance into distinct sub-metrics. Ragas (Retrieval Augmented Generation Assessment) isolates the Retriever component from the Generator (LLM) component using LLM-as-a-Judge prompting.

```text
                  ┌──────────────────────┐
                  │      User Query      │
                  └──────────┬───────────┘
                             │
                             ▼
 ┌────────────────────────────────────────────────────────┐
 │                   Retriever Component                  │
 └───────────────────────────┬────────────────────────────┘
                             │
                             ▼
                     Retrieved Context ──► [Context Recall / Context Precision]
                             │
                             ▼
 ┌────────────────────────────────────────────────────────┐
 │                   Generator Component                  │
 └───────────────────────────┬────────────────────────────┘
                             │
                             ▼
                     Generated Answer  ──► [Faithfulness & Answer Relevance]
```text

### The Core Ragas Metrics

#### 1. Faithfulness (Generation Safety / Hallucination Metric)

- **Measures:** Is the generated answer grounded strictly in the retrieved context?
- **Calculation:** The judge LLM extracts claims from the output answer and verifies what fraction of those claims can be directly inferred from the retrieved context.
- **Formula:**

$$\text{Faithfulness} = \frac{|\text{Verifiable Claims in Context}|}{|\text{Total Claims in Answer}|}$$

#### 2. Answer Relevance (Generation Focus Metric)

- **Measures:** Does the answer directly address the user's question, or does it wander off-topic?
- **Calculation:** The judge LLM generates $N$ synthetic questions based solely on the generated answer and computes cosine similarity between the original user query vector and the average vector of the generated questions.

#### 3. Context Recall (Retrieval Completeness Metric)

- **Measures:** Did the retriever fetch all relevant information required to answer the ground-truth reference?
- **Calculation:** Evaluates what percentage of sentences in the ground-truth answer can be attributed to the retrieved context chunks.

| Metric                | Component Evaluated | Requires Ground-Truth Reference? | Target Metric Goal                     |
| --------------------- | ------------------- | -------------------------------- | -------------------------------------- |
| **Faithfulness**      | Generator (LLM)     | No                               | 1.0 (Zero Hallucinations)              |
| **Answer Relevance**  | Generator (LLM)     | No                               | High (> 0.85)                          |
| **Context Precision** | Retriever           | No                               | High (Signal-to-noise ratio in chunks) |
| **Context Recall**    | Retriever           | Yes (Reference Ground Truth)     | 1.0 (Fetched all necessary facts)      |

## Example

Running automated Ragas evaluations in Python:

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevance, context_recall
from datasets import Dataset

# Sample evaluation batch
data = {
    "question": ["When was Python created and who authored it?"],
    "contexts": [["Python was conceived in the late 1980s by Guido van Rossum at CWI in the Netherlands."]],
    "answer": ["Python was created in the late 1980s by Guido van Rossum."],
    "ground_truth": ["Python was created in the late 1980s by Guido van Rossum."]
}

dataset = Dataset.from_dict(data)

results = evaluate(
    dataset=dataset,
    metrics=[
        faithfulness,
        answer_relevance,
        context_recall
    ]
)

print(results)
# Output: {'faithfulness': 1.0000, 'answer_relevance': 0.9652, 'context_recall': 1.0000}
```text

## Interview tips

- Highlight the "RAG Triad": Faithfulness, Answer Relevance, and Context Relevance.
- Explain how to fix failures based on metric signals: low Faithfulness means prompt tuning or system prompt guardrails needed; low Context Recall means embedding model, chunk size, or top-k retrieval strategy needs tuning.

---

[⬅ Back to Evaluation and Testing](./README.md) · [All topics](../README.md)
