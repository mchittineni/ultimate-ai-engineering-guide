---
title: "What is Cosine Similarity vs Euclidean Distance in vector search?"
id: 62
category: "RAG and Vector Databases"
difficulty: "Beginner"
tags:
  - ai-engineering
  - rag-and-vector-databases
  - interview-questions
---

# What is Cosine Similarity vs Euclidean Distance in vector search?

**Short answer:** Cosine similarity measures the angle between two embedding vectors regardless of magnitude (range $[-1, 1]$); Euclidean distance ($L_2$) measures the straight-line spatial distance between vector endpoints in $N$-dimensional space.

## Detail

Vector databases use similarity metrics to rank top-$K$ nearest neighbors:

### Formulas

1. **Cosine Similarity:**
   $$\cos(\theta) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|} = \frac{\sum A_i B_i}{\sqrt{\sum A_i^2} \sqrt{\sum B_i^2}}$$

2. **Euclidean Distance ($L_2$):**
   $$d(\mathbf{A}, \mathbf{B}) = \sqrt{\sum_{i=1}^N (A_i - B_i)^2}$$

3. **Dot Product (Inner Product):**
   $$\mathbf{A} \cdot \mathbf{B} = \sum_{i=1}^N A_i B_i$$

### Normalized Vector Identity

When embedding vectors are L2-normalized ($\|\mathbf{A}\| = \|\mathbf{B}\| = 1$), Cosine Similarity, Dot Product, and Euclidean distance become mathematically equivalent ordering operations:

$$d_{Euclidean}^2(\mathbf{A}, \mathbf{B}) = 2 - 2 \cdot \cos(\theta)$$

## Example

NumPy vector metrics comparison:

```python
import numpy as np

a = np.array([1.0, 2.0, 3.0])
b = np.array([2.0, 4.0, 6.0]) # Same direction, double magnitude

# Cosine similarity ignores magnitude -> perfect 1.0 match
cos_sim = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Euclidean distance accounts for magnitude -> non-zero distance
l2_dist = np.linalg.norm(a - b)

print("Cosine Similarity:", cos_sim)
print("Euclidean Distance:", l2_dist)
```

## Interview tips

- Highlight that OpenAI embeddings are L2-normalized, making Dot Product faster to compute than full Cosine similarity.
- Note that for text retrieval, Cosine similarity is preferred because it focuses on semantic direction rather than document length magnitude.

---

[⬅ Back to RAG and Vector Databases](./README.md) · [All topics](../README.md)
