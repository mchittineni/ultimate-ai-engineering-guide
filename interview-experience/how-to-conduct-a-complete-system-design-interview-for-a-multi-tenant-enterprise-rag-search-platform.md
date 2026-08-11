---
title: "How to conduct a complete system design interview for a multi-tenant enterprise RAG search platform?"
id: 199
category: "Interview Experience"
difficulty: "Advanced"
tags:
  - ai-engineering
  - interview-experience
  - interview-questions
---

# How to conduct a complete system design interview for a multi-tenant enterprise RAG search platform?

**Short answer:** Conduct an enterprise RAG system design interview by outlining an end-to-end multi-tenant architecture: API Gateway with RBAC pre-filtering, document ingestion pipeline with vision layout parsing, hybrid vector/sparse search with cross-encoder reranking, vLLM serving with PagedAttention and prefix caching, and continuous Ragas evaluation telemetry.

## Detail

This advanced scenario tests a candidate's ability to synthesize all major sub-systems of enterprise AI engineering into a single coherent blueprint.

```
[Enterprise Web Clients]
           │
           ▼
[API Gateway] ──► RBAC Tenant Token Validation (OAuth 2.0)
           │
           ├──► [Redis Semantic Cache] (Hit -> Return Instant Response)
           │
           ▼ (Cache Miss)
[Hybrid Retrieval Engine]
 ├── Sparse Search (BM25 for exact SKU/part codes)
 ├── Dense Vector Search (Qdrant with RBAC Pre-Filtering)
 └── Cross-Encoder Reranker (Cohere Rerank v3)
           │
           ▼
[vLLM Inference Cluster] (PagedAttention + Chunked Prefill + Prefix Cache)
           │
           ▼
[Output Guardrail & Telemetry] ──► DeBERTa NLI Entailment Check + OpenTelemetry Spans
```

### Complete Sub-System Checklist

1. **Ingestion Pipeline:** Parsing PDFs/DOCX using layout parsers, embedding via Matryoshka models, attaching RBAC tenant metadata.
2. **Retrieval Pipeline:** Hybrid BM25 + HNSW vector search merged via Reciprocal Rank Fusion (RRF), passed to cross-encoder reranker.
3. **Inference Pipeline:** Disaggregated prefill/decoding clusters running vLLM with PagedAttention and prefix caching.
4. **Governance & Observability:** Reversible PII redactor, OpenTelemetry tracing, and Ragas evaluation benchmarks.

## Example

Whiteboard architecture blueprint summary:

```markdown
1. Security Layer: PII Redaction Proxy + Tenant Isolation RBAC Pre-Filter.
2. Search Layer: Hybrid BM25 + Dense Vectors merged via RRF (k=60) + Cross-Encoder Rerank.
3. Generation Layer: vLLM Inference Engine with PagedAttention & Speculative Decoding.
4. Quality Layer: NLI Entailment Hallucination Guardrail + Continuous Ragas Evaluation.
```

## Interview tips

- Cover every phase of the architecture systematically without skipping security or observability.
- Highlight scaling bottlenecks (e.g. KV cache VRAM pressure under peak concurrent user load) and how PagedAttention solves them.

## Related Concepts

- [[What is document metadata filtering in vector databases?]] (`#123`): [What is document metadata filtering in vector databases?](../rag-and-vector-databases/what-is-document-metadata-filtering-in-vector-databases.md)
- [[How does Reciprocal Rank Fusion (RRF) combine scores from sparse and dense retrievers?]] (`#127`): [How does Reciprocal Rank Fusion (RRF) combine scores from sparse and dense retrievers?](../rag-and-vector-databases/how-does-reciprocal-rank-fusion-rrf-combine-scores-from-sparse-and-dense-retrievers.md)
- [[How does vLLM PagedAttention manage Virtual Memory Pages to eliminate KV cache fragmentation?]] (`#159`): [How does vLLM PagedAttention manage Virtual Memory Pages to eliminate KV cache fragmentation?](../ai-system-design/how-does-vllm-pagedattention-manage-virtual-memory-pages-to-eliminate-kv-cache-fragmentation.md)

---

[⬅ Back to Interview Experience](./README.md) · [All topics](../README.md)
