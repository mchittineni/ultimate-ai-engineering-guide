---
title: "How do cross-encoder rerankers and late-interaction (ColBERT) models work?"
id: 22
category: "RAG and Vector Databases"
difficulty: "Advanced"
tags:
  - ai-engineering
  - rag-and-vector-databases
  - interview-questions
---

# How do cross-encoder rerankers and late-interaction (ColBERT) models work?

**Short answer:** Bi-encoders project query and document into separate single vectors for fast approximate nearest neighbor (ANN) search; cross-encoders process the query and document jointly through full Transformer self-attention layers for max accuracy at higher computational cost; late-interaction models (ColBERT) retain token-level embeddings and compute fine-grained MaxSim vector alignment to bridge speed and accuracy.

## Detail

Retrieval architecture follows a multi-stage funnel:

```
[Candidate Documents: 10,000+]
            │
   (Bi-Encoder / Hybrid Search) ──► Fast ANN search
            │
  [Top 100 Candidates]
            │
   (Cross-Encoder Reranker)    ──► Deep self-attention cross-scoring
            │
   [Top 5 Grounded Contexts]
```

### Architecture Comparison

| Model Type | Representation | Query-Doc Attention | Latency | Accuracy |
| --- | --- | --- | --- | --- |
| **Bi-Encoder** | Single vector per doc | No cross-attention (dot product / cosine) | Low (~5-10ms) | Good |
| **Cross-Encoder** | Joint classification | Full cross-attention ($Q \leftrightarrow Doc$) | High (~50-200ms) | Highest |
| **ColBERT (Late-Interaction)** | Multi-vector matrix per doc | Token-level MaxSim dot product | Medium (~15-30ms) | Near Cross-Encoder |

### ColBERT MaxSim Calculation

$$\text{Score}(Q, D) = \sum_{i \in |Q|} \max_{j \in |D|} \left( E_{q,i} \cdot E_{d,j}^T \right)$$

Each query token vector $E_{q,i}$ finds its maximum dot product match across all document token vectors $E_{d,j}$.

## Example

Conceptual Python snippet illustrating Cross-Encoder score evaluation:

```python
# Cross-encoder joint input formatting:
def format_cross_encoder_input(query: str, doc_text: str) -> str:
    return f"[CLS] {query} [SEP] {doc_text} [SEP]"

# Fast dot product (Bi-encoder) vs Joint forward pass (Cross-encoder)
query = "What is KV cache latency?"
doc = "KV caching stores key value tensors in GPU VRAM to reduce token generation time."

print("Cross-encoder pair sequence:", format_cross_encoder_input(query, doc))
```

## Interview tips

- Explain why cross-encoders cannot be pre-indexed into a vector DB: document representations depend on the query string passed at runtime.
- Highlight Cohere Rerank or `bge-reranker-large` as standard production reranking components in advanced RAG pipelines.

---

[⬅ Back to RAG and Vector Databases](./README.md) · [All topics](../README.md)
