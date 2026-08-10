---
title: "How do dense and sparse vector embeddings differ?"
id: 20
category: "RAG and Vector Databases"
difficulty: "Beginner"
tags:
  - ai-engineering
  - rag-and-vector-databases
  - interview-questions
---

# How do dense and sparse vector embeddings differ?

**Short answer:** Dense embeddings represent text using continuous, fixed-size floating-point vectors (e.g., 768 or 1536 dimensions) where most values are non-zero to capture semantic meaning; sparse embeddings (e.g., BM25, SPLADE) use high-dimensional vectors (e.g., 30,000+ dimensions) where most values are zero to capture exact keyword matches and term frequencies.

## Detail

Retrieval systems rely on complementary embedding paradigms to maximize search recall and precision.

| Characteristic          | Dense Embeddings                                       | Sparse Embeddings                                         |
| ----------------------- | ------------------------------------------------------ | --------------------------------------------------------- |
| **Dimensionality**      | Low to medium (384 – 3072 dims)                        | High (vocabulary size, e.g., 30,000+ dims)                |
| **Values**              | Non-zero float32 / float16 values                      | Mostly zero values (sparse matrix)                        |
| **Primary Strength**    | Semantic similarity, synonyms, intent matching         | Exact keyword matching, product IDs, rare jargon          |
| **Weakness**            | Can miss exact out-of-vocabulary product SKUs or names | Cannot recognize synonyms (e.g., "physician" vs "doctor") |
| **Algorithms / Models** | OpenAI `text-embedding-3-small`, BGE-large, E5         | BM25, TF-IDF, SPLADE                                      |

Combining dense and sparse embeddings via Hybrid Search produces the highest retrieval accuracy in production RAG systems.

## Example

Comparing representation types in Python:

```python
import numpy as np

# Dense vector: Fixed length (4 dims for illustration), all non-zero
dense_vector = np.array([0.14, -0.82, 0.45, 0.91], dtype=np.float32)

# Sparse vector: Dictionary mapping vocabulary index -> term score (e.g., BM25)
# Dimension is 30,000 (vocab size), but only 2 terms exist in text
sparse_vector = {1402: 2.45, 8912: 1.12}

print("Dense vector shape:", dense_vector.shape)
print("Sparse non-zero count:", len(sparse_vector))
```

## Interview tips

- Highlight that dense vectors struggle with exact string searches (e.g., part numbers like `"ERR-9021"`), whereas sparse vectors excel.
- Explain how hybrid search uses Reciprocal Rank Fusion (RRF) to merge dense and sparse result lists.

---

[⬅ Back to RAG and Vector Databases](./README.md) · [All topics](../README.md)
