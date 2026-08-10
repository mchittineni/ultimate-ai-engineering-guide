---
title: "What is context precision vs context recall in RAG?"
id: 86
category: "Evaluation and Testing"
difficulty: "Beginner"
tags:
  - ai-engineering
  - evaluation-and-testing
  - interview-questions
---

# What is context precision vs context recall in RAG?

**Short answer:** Context Precision measures the signal-to-noise ratio of retrieved chunks (how many of the retrieved passages were actually relevant); Context Recall measures whether all the ground-truth information necessary to answer the prompt was successfully retrieved.

## Detail

Evaluating the retrieval stage of a RAG pipeline requires separating retrieval precision from generation quality (e.g. in the Ragas evaluation framework).

```text
Retrieved Context Chunks: [Chunk 1 (Relevant), Chunk 2 (Irrelevant), Chunk 3 (Irrelevant)]
  ├── Context Precision = Low (1/3 relevant chunks = high noise)
  └── Context Recall    = High (if Chunk 1 contains ALL necessary facts)
```

| Metric                | Focus Question                                                            | Target Metric Optimization                                           |
| --------------------- | ------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| **Context Precision** | _"Are top-ranked chunks actually relevant, or did we retrieve clutter?"_  | Optimizes rank position (Rerankers, higher similarity thresholds)    |
| **Context Recall**    | _"Did the retriever find all key facts required to answer the question?"_ | Optimizes recall search (Increasing $K$, hybrid search BM25 + Dense) |

### Context Precision Formula (Ragas)

$$\text{Context Precision@K} = \frac{\sum_{k=1}^K \text{Precision@k} \times v_k}{\text{Total Relevant Chunks in Top K}}$$

Where $v_k \in \{0, 1\}$ indicates if chunk $k$ is relevant.

## Example

Python concept evaluating context recall against ground truth statements:

```python
def calculate_context_recall(ground_truth_statements: list[str], retrieved_context: str) -> float:
    # Check what fraction of required ground truth facts exist in retrieved context
    found = 0
    for stmt in ground_truth_statements:
        if stmt.lower() in retrieved_context.lower():
            found += 1
    return found / len(ground_truth_statements) if ground_truth_statements else 0.0

gt = ["Server restarted at 02:00 UTC", "Error code was 503"]
context = "System logs show server restarted at 02:00 UTC due to maintenance."
print("Context Recall:", calculate_context_recall(gt, context)) # 0.5 (1 of 2 facts retrieved)
```

## Interview tips

- Emphasize that high context recall prevents hallucinations, while high context precision reduces prompt token costs and latency.
- Connect this to the Ragas evaluation trilemma (Faithfulness, Context Recall, Answer Relevance).

---

[⬅ Back to Evaluation and Testing](./README.md) · [All topics](../README.md)
