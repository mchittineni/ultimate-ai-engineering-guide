---
title: "How do GraphRAG and Knowledge Graphs enhance vector retrieval?"
id: 65
category: "RAG and Vector Databases"
difficulty: "Advanced"
tags:
  - ai-engineering
  - rag-and-vector-databases
  - interview-questions
---

# How do GraphRAG and Knowledge Graphs enhance vector retrieval?

**Short answer:** GraphRAG extracts structured entities and relationships from text into a Knowledge Graph (KG), combining vector similarity search with graph traversal (multi-hop relational querying and community summarization) to answer global dataset questions that standard vector retrieval misses.

## Detail

Standard vector RAG excels at localized passage retrieval (e.g. _"What is Company X's Q3 revenue?"_), but struggles with global, holistic dataset queries (e.g. _"What are the top 5 overarching themes across all 500 customer support transcripts?"_).

```text
Unstructured Text ──► [LLM Entity Extractor] ──► Knowledge Graph (Nodes & Edges)
                                                       │
[User Query] ──► Vector Search + Graph Traversal (Sub-graph extraction) ──► Global Summary
```

### Core Architecture of GraphRAG

1. **Entity & Relationship Extraction:** An LLM parses text to extract entities (Nodes: `Person`, `Product`, `Org`) and relationships (Edges: `WORKS_AT`, `VULNERABLE_TO`).
2. **Community Detection:** Algorithms (e.g. Leiden algorithm) cluster graph nodes into hierarchical communities.
3. **Community Summarization:** LLMs generate pre-computed summaries for each community level.
4. **Hybrid Graph Retrieval:** At query time, GraphRAG queries graph community summaries alongside dense vector indexes.

## Example

Conceptual Cypher (Neo4j) query combining graph traversal with vector scoring:

```cypher
// GraphRAG hybrid retrieval example
MATCH (c:Company {name: "Acme Corp"})-[:PRODUCES]->(p:Product)-[:HAS_VULNERABILITY]->(v:Vulnerability)
RETURN c.name, p.name, v.severity
ORDER BY v.severity DESC LIMIT 5
```

## Interview tips

- Highlight that GraphRAG significantly reduces hallucinations for multi-hop relational reasoning questions.
- Emphasize the trade-off: GraphRAG requires expensive LLM processing during indexing to construct graphs and community summaries.

---

[⬅ Back to RAG and Vector Databases](./README.md) · [All topics](../README.md)
