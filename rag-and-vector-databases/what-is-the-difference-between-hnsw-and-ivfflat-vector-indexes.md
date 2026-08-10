---
title: "What is the difference between HNSW and IVFFlat vector indexes?"
id: 4
category: "RAG and Vector Databases"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - rag-and-vector-databases
  - interview-questions
---

# What is the difference between HNSW and IVFFlat vector indexes?

**Short answer:** HNSW (Hierarchical Navigable Small World) builds a multi-layer graph for fast, high-recall vector search at the cost of higher RAM usage, whereas IVFFlat (Inverted File Flat) clusters vector space into Voronoi cells to save memory at the cost of lower query throughput and index build speed.

## Detail

Exact Nearest Neighbor (kNN) search requires computing vector distance against every document in the database, scaling as $O(N \cdot D)$. Approximate Nearest Neighbor (ANN) indexes trade a tiny fraction of search recall to achieve sub-linear $O(\log N)$ query speed.

### HNSW (Hierarchical Navigable Small World)

HNSW is a graph-based indexing algorithm inspired by skip-lists:

- **Structure:** Builds a multi-layer graph where top layers have long-range links for fast coarse navigation across vector space, while lower layers have short-range links for fine-grained local search.
- **Querying:** Search starts at the top layer, greedily traverses long edges, steps down a layer when no closer neighbor exists, and reaches the bottom layer for precise final candidates.
- **Pros:** Ultra-fast query latency (<5ms) and extremely high recall (>95-98%).
- **Cons:** Heavy RAM footprint (requires storing graph edges alongside vectors) and slow index build times.

### IVFFlat (Inverted File Flat)

IVFFlat is a cluster-based partitioning index:

- **Structure:** Uses k-means clustering to divide vector space into $N_{list}$ Voronoi centroids. Vectors are assigned to their nearest centroid.
- **Querying:** When a search query arrives, IVFFlat calculates distance to all $N_{list}$ centroids, selects the top $N_{probe}$ nearest clusters, and performs exhaustive distance checks only within those clusters.
- **Pros:** Low memory overhead, fast index build time, easy to combine with Product Quantization (IVF-PQ).
- **Cons:** Lower recall if $N_{probe}$ is too small; increasing $N_{probe}$ improves accuracy but reduces query throughput.

| Dimension              | HNSW                                       | IVFFlat                                     |
| ---------------------- | ------------------------------------------ | ------------------------------------------- |
| **Index Type**         | Multi-layer Graph                          | Inverted File Index (Clustering)            |
| **Memory (RAM) Usage** | High (1.5x - 2x raw vector footprint)      | Low (Raw vectors + small centroid table)    |
| **Query Latency**      | Extremely Low (< 5ms)                      | Low to Medium (depends on `nprobe`)         |
| **Recall Rate**        | 95% - 99%+                                 | 85% - 95%                                   |
| **Index Build Speed**  | Slow                                       | Fast                                        |
| **Ideal Use Case**     | Real-time user queries, high precision RAG | Billions of vectors, cost-constrained infra |

## Example

Configuration in PGVector / Qdrant / FAISS:

```python
import faiss
import numpy as np

dimension = 1536  # OpenAI text-embedding-3-small dimension
num_vectors = 100000
data = np.random.random((num_vectors, dimension)).astype('float32')

# 1. HNSW Index Setup
M = 32              # Graph connectivity parameter (number of bidirectional links per node)
efConstruction = 64 # Depth of search during index build
index_hnsw = faiss.IndexHNSWFlat(dimension, M)
index_hnsw.hnsw.efConstruction = efConstruction
index_hnsw.add(data)

# 2. IVFFlat Index Setup
nlist = 100         # Number of Voronoi clusters
quantizer = faiss.IndexFlatL2(dimension)
index_ivf = faiss.IndexIVFFlat(quantizer, dimension, nlist)
index_ivf.train(data)
index_ivf.add(data)
index_ivf.nprobe = 10 # Number of clusters inspected at query time
```

## Interview tips

- Always explain the tradeoff parameters: `M` and `efSearch` for HNSW vs `nlist` and `nprobe` for IVFFlat.
- Mention hybrid techniques: Combining IVF with Product Quantization (IVF-PQ) or Scalar Quantization (HNSW-SQ8) to cut vector RAM requirements by 4x to 8x in production.

---

[⬅ Back to RAG and Vector Databases](./README.md) · [All topics](../README.md)
