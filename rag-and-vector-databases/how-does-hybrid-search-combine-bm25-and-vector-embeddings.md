---
title: "How does hybrid search combine BM25 and vector embeddings?"
id: 21
category: "RAG and Vector Databases"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - rag-and-vector-databases
  - interview-questions
---

# How does hybrid search combine BM25 and vector embeddings?

**Short answer:** Hybrid search runs exact keyword matching (BM25 sparse search) and semantic similarity search (dense vector search) in parallel, merging their ranked result sets using algorithms like Reciprocal Rank Fusion (RRF) or relative score normalization.

## Detail

Pure dense search often misses exact alphanumeric matches (e.g., error codes `"ERR-503"`, user IDs, model part numbers), while pure BM25 fails to match conceptual synonyms (e.g., `"automobile"` vs `"car"`). Hybrid search mitigates the failure modes of both.

### Reciprocal Rank Fusion (RRF)

Rather than directly summing raw similarity scores (which operate on different scales), RRF combines candidate document rankings:

$$RRF\_Score(d \in D) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$

Where:
- $M$ is the set of retrieval systems (Dense and Sparse).
- $r_m(d)$ is the rank position of document $d$ in retriever $m$.
- $k$ is a smoothing constant (typically $k=60$).

RRF is robust because it relies only on rank position rather than uncalibrated raw score distributions.

## Example

Python implementation of Reciprocal Rank Fusion:

```python
def reciprocal_rank_fusion(dense_ranks: list[str], sparse_ranks: list[str], k: int = 60) -> list[tuple[str, float]]:
    rrf_scores = {}

    for rank, doc_id in enumerate(dense_ranks, start=1):
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k + rank))

    for rank, doc_id in enumerate(sparse_ranks, start=1):
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k + rank))

    sorted_docs = sorted(rrf_scores.items(), key=lambda item: item[1], reverse=True)
    return sorted_docs

# Example doc IDs ranked by dense and sparse retrievers
dense = ["doc_A", "doc_B", "doc_C"]
sparse = ["doc_B", "doc_D", "doc_A"]

print("RRF Combined Results:", reciprocal_rank_fusion(dense, sparse))
```

## Interview tips

- Note that modern vector databases (e.g., Qdrant, Pinecone, Milvus, Weaviate) offer native hybrid search with built-in RRF.
- Mention combining hybrid search with a cross-encoder reranker for maximum retrieval precision.

---

[⬅ Back to RAG and Vector Databases](./README.md) · [All topics](../README.md)
