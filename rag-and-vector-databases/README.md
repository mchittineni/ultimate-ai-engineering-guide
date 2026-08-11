---
title: "RAG and Vector Databases"
category: "RAG and Vector Databases"
tags:
  - ai-engineering
  - rag-and-vector-databases
  - index
---

# RAG and Vector Databases

Embeddings, vector indexing (HNSW, IVFFlat), hybrid search, chunking strategies, re-ranking, and query transformation.

**20 questions** · 🟢 Beginner: 10 · 🟡 Intermediate: 6 · 🔴 Advanced: 4

## Questions

| #   | Question                                                                                                                                                                                                               | Difficulty      |
| --- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 4   | [What is the difference between HNSW and IVFFlat vector indexes?](./what-is-the-difference-between-hnsw-and-ivfflat-vector-indexes.md)                                                                                 | 🟡 Intermediate |
| 19  | [What is Retrieval-Augmented Generation (RAG) and why is it used?](./what-is-retrieval-augmented-generation-rag-and-why-is-it-used.md)                                                                                 | 🟢 Beginner     |
| 20  | [How do dense and sparse vector embeddings differ?](./how-do-dense-and-sparse-vector-embeddings-differ.md)                                                                                                             | 🟢 Beginner     |
| 21  | [How does hybrid search combine BM25 and vector embeddings?](./how-does-hybrid-search-combine-bm25-and-vector-embeddings.md)                                                                                           | 🟡 Intermediate |
| 22  | [How do cross-encoder rerankers and late-interaction (ColBERT) models work?](./how-do-cross-encoder-rerankers-and-late-interaction-colbert-models-work.md)                                                             | 🔴 Advanced     |
| 61  | [What is chunk size and chunk overlap in text splitting?](./what-is-chunk-size-and-chunk-overlap-in-text-splitting.md)                                                                                                 | 🟢 Beginner     |
| 62  | [What is Cosine Similarity vs Euclidean Distance in vector search?](./what-is-cosine-similarity-vs-euclidean-distance-in-vector-search.md)                                                                             | 🟢 Beginner     |
| 63  | [What is the 'Lost in the Middle' phenomenon in LLM retrieval?](./what-is-the-lost-in-the-middle-phenomenon-in-llm-retrieval.md)                                                                                       | 🟢 Beginner     |
| 64  | [How does query rewriting and Hypothetical Document Embeddings (HyDE) work?](./how-does-query-rewriting-and-hypothetical-document-embeddings-hyde-work.md)                                                             | 🟡 Intermediate |
| 65  | [How do GraphRAG and Knowledge Graphs enhance vector retrieval?](./how-do-graphrag-and-knowledge-graphs-enhance-vector-retrieval.md)                                                                                   | 🔴 Advanced     |
| 121 | [What is an embedding model and how does vector dimension affect search quality?](./what-is-an-embedding-model-and-how-does-vector-dimension-affect-search-quality.md)                                                 | 🟢 Beginner     |
| 122 | [What is semantic search and how does it differ from traditional keyword search?](./what-is-semantic-search-and-how-does-it-differ-from-traditional-keyword-search.md)                                                 | 🟢 Beginner     |
| 123 | [What is document metadata filtering in vector databases?](./what-is-document-metadata-filtering-in-vector-databases.md)                                                                                               | 🟢 Beginner     |
| 124 | [What is single-representation vs multi-representation document retrieval?](./what-is-single-representation-vs-multi-representation-document-retrieval.md)                                                             | 🟢 Beginner     |
| 125 | [What is document parsing and why do table formats break standard text splitters?](./what-is-document-parsing-and-why-do-table-formats-break-standard-text-splitters.md)                                               | 🟢 Beginner     |
| 126 | [How does Parent-Document Retrieval link fine-grained vector chunks back to full parent context?](./how-does-parent-document-retrieval-link-fine-grained-vector-chunks-back-to-full-parent-context.md)                 | 🟡 Intermediate |
| 127 | [How does Reciprocal Rank Fusion (RRF) combine scores from sparse and dense retrievers?](./how-does-reciprocal-rank-fusion-rrf-combine-scores-from-sparse-and-dense-retrievers.md)                                     | 🟡 Intermediate |
| 128 | [How does contextual compression reduce context window token usage during RAG?](./how-does-contextual-compression-reduce-context-window-token-usage-during-rag.md)                                                     | 🟡 Intermediate |
| 129 | [How does RAPTOR perform hierarchical tree-organized retrieval?](./how-does-raptor-perform-hierarchical-tree-organized-retrieval.md)                                                                                   | 🔴 Advanced     |
| 130 | [How does Self-RAG train models to dynamically decide when to retrieve, evaluate, and critique documents?](./how-does-self-rag-train-models-to-dynamically-decide-when-to-retrieve-evaluate-and-critique-documents.md) | 🔴 Advanced     |

## What interviewers probe here

- Dense vs sparse embeddings and hybrid keyword + semantic search.
- Chunking strategies (semantic, sliding window) and document parsing.
- HNSW vs IVFFlat index tradeoffs for latency, memory, and recall.

---

[⬅ Back to all topics](../README.md)
