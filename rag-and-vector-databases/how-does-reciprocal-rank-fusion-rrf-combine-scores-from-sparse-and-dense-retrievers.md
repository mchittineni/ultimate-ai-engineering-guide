---
title: "How does Reciprocal Rank Fusion (RRF) combine scores from sparse and dense retrievers?"
id: 127
category: "RAG and Vector Databases"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - rag-and-vector-databases
  - interview-questions
---

# How does Reciprocal Rank Fusion (RRF) combine scores from sparse and dense retrievers?

**Short answer:** Reciprocal Rank Fusion (RRF) is an algorithm that merges search results from multiple independent retrieval systems (e.g. BM25 keyword search and dense vector search) by calculating a combined score based on each document's reciprocal rank position across query result lists, requiring zero score normalization.

## Detail

Dense vector scores (cosine similarity $[0, 1]$) and BM25 sparse scores ($[0, \infty)$) operate on incompatible scale distributions. Direct score addition fails.

### RRF Formula

$$\text{RRF\_Score}(d \in D) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$

Where:

- $M$ is the set of retrieval algorithms (e.g. BM25, Vector Search).
- $r_m(d)$ is the 1-based rank position of document $d$ in retriever $m$'s result list.
- $k$ is a smoothing constant (standard default $k = 60$).

```text
Document A: BM25 Rank 1, Vector Rank 5  ──► RRF = 1/(60+1) + 1/(60+5) = 0.01639 + 0.01538 = 0.03177
Document B: BM25 Rank 20, Vector Rank 1 ──► RRF = 1/(60+20) + 1/(60+1) = 0.01250 + 0.01639 = 0.02889
```

## Example

Python RRF merger implementation:

```python
def reciprocal_rank_fusion(results_list: list[list[str]], k: int = 60) -> list[tuple[str, float]]:
    rrf_scores = {}
    for results in results_list:
        for rank, doc_id in enumerate(results, start=1):
            if doc_id not in rrf_scores:
                rrf_scores[doc_id] = 0.0
            rrf_scores[doc_id] += 1.0 / (k + rank)

    # Sort documents by combined RRF score descending
    sorted_docs = sorted(rrf_scores.items(), key=lambda item: item[1], reverse=True)
    return sorted_docs

bm25_res = ["doc1", "doc2", "doc3"]
vector_res = ["doc2", "doc1", "doc4"]
print("RRF Combined Rankings:", reciprocal_rank_fusion([bm25_res, vector_res]))
```

## Interview tips

- Explain why RRF is robust: it relies strictly on rank order rather than raw similarity score magnitudes, eliminating score scaling skew between different embedding models or search engines.
- Highlight using RRF prior to passing candidates to a cross-encoder reranker.

## Related Concepts

- [[What is semantic search and how does it differ from traditional keyword search?]] (`#122`): [What is semantic search and how does it differ from traditional keyword search?](../rag-and-vector-databases/what-is-semantic-search-and-how-does-it-differ-from-traditional-keyword-search.md)
- [[How to build an automated RAG evaluation harness measuring Context Precision and Recall?]] (`#178`): [How to build an automated RAG evaluation harness measuring Context Precision and Recall?](../evaluation-and-testing/how-to-build-an-automated-rag-evaluation-harness-measuring-context-precision-and-recall.md)
- [[How to conduct a complete system design interview for a multi-tenant enterprise RAG search platform?]] (`#199`): [How to conduct a complete system design interview for a multi-tenant enterprise RAG search platform?](../interview-experience/how-to-conduct-a-complete-system-design-interview-for-a-multi-tenant-enterprise-rag-search-platform.md)

---

[⬅ Back to RAG and Vector Databases](./README.md) · [All topics](../README.md)
