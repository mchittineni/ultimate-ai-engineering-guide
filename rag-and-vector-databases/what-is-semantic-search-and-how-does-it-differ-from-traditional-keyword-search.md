---
title: "What is semantic search and how does it differ from traditional keyword search?"
id: 122
category: "RAG and Vector Databases"
difficulty: "Beginner"
tags:
  - ai-engineering
  - rag-and-vector-databases
  - interview-questions
---

# What is semantic search and how does it differ from traditional keyword search?

**Short answer:** Semantic search retrieves documents based on conceptual meaning and intent in vector space regardless of exact word overlap; traditional keyword search (e.g. BM25 / TF-IDF) relies on exact lexical string matching between query and document tokens.

## Detail

Keyword search struggles when users ask queries using synonyms, misspellings, or alternative phrasing.

```text
Query: "How to fix a leaky faucet?"
Keyword Search (BM25): Looks for exact strings "fix", "leaky", "faucet". Misses "Repair dripping tap".
Semantic Search:       Embeds query intent -> Retrieves "Guide to repairing a dripping water tap".
```

### Core Comparison

| Metric                    | Lexical Keyword Search (BM25)               | Semantic Vector Search                                   |
| ------------------------- | ------------------------------------------- | -------------------------------------------------------- |
| **Matching Mechanism**    | Exact token string overlap                  | Distance between vector embeddings                       |
| **Synonym Awareness**     | Poor (Requires manual synonym dictionaries) | High (Inherent in pre-trained embeddings)                |
| **Domain-Specific Terms** | High (Excels at exact part numbers / SKUs)  | Moderate (Can miss rare exact codes without fine-tuning) |
| **Index Type**            | Inverted Index                              | HNSW / IVFFlat Graph Indexes                             |

## Example

Comparing BM25 lexical match vs Cosine vector similarity in Python:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

docs = ["How to fix a dripping water tap", "Database index optimization guide"]
query = "repair leaky faucet"

# Lexical TF-IDF match (Zero overlap -> 0 score)
tfidf = TfidfVectorizer()
matrix = tfidf.fit_transform([query] + docs)
scores = (matrix[0] * matrix[1:].T).toarray()
print("Lexical Match Scores:", scores) # Returns 0.0 for both because exact words don't match
```

## Interview tips

- Highlight why enterprise RAG systems use **Hybrid Search** (combining BM25 for exact SKU codes + Dense Vectors for semantic intent).
- Explain cross-encoder reranking as the final stage of hybrid search pipelines.

## Related Concepts

- [[How does Reciprocal Rank Fusion (RRF) combine scores from sparse and dense retrievers?]] (`#127`): [How does Reciprocal Rank Fusion (RRF) combine scores from sparse and dense retrievers?](../rag-and-vector-databases/how-does-reciprocal-rank-fusion-rrf-combine-scores-from-sparse-and-dense-retrievers.md)
- [[How to enforce Role-Based Access Control (RBAC) filtering in multi-tenant RAG vector search?]] (`#188`): [How to enforce Role-Based Access Control (RBAC) filtering in multi-tenant RAG vector search?](../ai-safety-and-governance/how-to-enforce-role-based-access-control-rbac-filtering-in-multi-tenant-rag-vector-search.md)
- [[How to answer scenario questions about trade-offs between RAG and Fine-Tuning?]] (`#194`): [How to answer scenario questions about trade-offs between RAG and Fine-Tuning?](../interview-experience/how-to-answer-scenario-questions-about-trade-offs-between-rag-and-fine-tuning.md)

---

[⬅ Back to RAG and Vector Databases](./README.md) · [All topics](../README.md)
