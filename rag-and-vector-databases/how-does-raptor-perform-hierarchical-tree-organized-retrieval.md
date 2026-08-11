---
title: "How does RAPTOR perform hierarchical tree-organized retrieval?"
id: 129
category: "RAG and Vector Databases"
difficulty: "Advanced"
tags:
  - ai-engineering
  - rag-and-vector-databases
  - interview-questions
---

# How does RAPTOR perform hierarchical tree-organized retrieval?

**Short answer:** RAPTOR (Recursive Abstractive Processing for Tree-Organized Retrieval) recursively clusters text chunks, generates abstractive LLM summaries for each cluster, and indexes both raw chunks and multi-level summary nodes into a hierarchical tree structure, enabling RAG systems to answer high-level holistic questions alongside low-level detail queries.

## Detail

Standard vector retrieval indexes isolated text chunks, failing on high-level thematic queries (e.g. *"What are the key overarching themes across the entire 300-page report?"*).

```
Level 2 (Global Summary):                  [ Root Summary Node ]
                                            /                  \
Level 1 (Cluster Summaries):     [ Cluster Summary A ]    [ Cluster Summary B ]
                                  /         |         \     /         \
Level 0 (Raw Text Chunks):   [Chunk 1]  [Chunk 2]  [Chunk 3] [Chunk 4] [Chunk 5]
```

### RAPTOR Tree Construction Algorithm

1. **Leaf Chunks (Level 0):** Segment document into standard text chunks (e.g. 100 tokens).
2. **Soft Clustering:** Cluster chunk embeddings using Gaussian Mixture Models (GMMs) or UMAP dimensionality reduction.
3. **Summarization:** Use an LLM to generate a summary for each cluster.
4. **Recursive Indexing:** Embed summary nodes and repeat clustering recursively until a root summary is reached.
5. **Collapsed Tree Retrieval:** Search across all levels (leaf chunks + multi-level summaries) simultaneously during query execution.

## Example

Conceptual Python data model for a RAPTOR hierarchical node:

```python
class RAPTORNode:
    def __init__(self, node_id: str, text: str, level: int, children: list[str] = None):
        self.node_id = node_id
        self.text = text
        self.level = level # Level 0 = raw chunk, Level 1+ = summary
        self.children = children or []

# Level 1 summary node linking to 2 raw Level 0 leaf chunks
summary_node = RAPTORNode(
    node_id="summary_lvl1_04",
    text="Executive summary of Q3 financial performance across departments...",
    level=1,
    children=["chunk_001", "chunk_002"]
)
```

## Interview tips

- Contrast RAPTOR with GraphRAG: RAPTOR builds hierarchical text summary trees, while GraphRAG extracts entity-relationship knowledge graphs.
- Highlight RAPTOR's benchmark performance gains on long-context QA benchmarks (QASPER, QuALITY).

## Related Concepts

- [[How does Graph-of-Thoughts (GoT) extend Tree-of-Thoughts for arbitrary network reasoning?]] (`#119`): [How does Graph-of-Thoughts (GoT) extend Tree-of-Thoughts for arbitrary network reasoning?](../prompt-engineering/how-does-graph-of-thoughts-got-extend-tree-of-thoughts-for-arbitrary-network-reasoning.md)
- [[What is single-representation vs multi-representation document retrieval?]] (`#124`): [What is single-representation vs multi-representation document retrieval?](../rag-and-vector-databases/what-is-single-representation-vs-multi-representation-document-retrieval.md)
- [[How to conduct a complete system design interview for a multi-tenant enterprise RAG search platform?]] (`#199`): [How to conduct a complete system design interview for a multi-tenant enterprise RAG search platform?](../interview-experience/how-to-conduct-a-complete-system-design-interview-for-a-multi-tenant-enterprise-rag-search-platform.md)

---

[⬅ Back to RAG and Vector Databases](./README.md) · [All topics](../README.md)
