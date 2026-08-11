---
title: "How to lead an ambiguous AI system design interview from requirements to architecture?"
id: 196
category: "Interview Experience"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - interview-experience
  - interview-questions
---

# How to lead an ambiguous AI system design interview from requirements to architecture?

**Short answer:** Lead ambiguous AI system design interviews by systematically establishing functional and non-functional requirements (QPS, TTFT/TPOT SLAs, token budget), calculating back-of-the-envelope GPU/VRAM estimations, diagramming high-level data flow topology, justifying technical trade-offs, and detailing failure mode resilience.

## Detail

In staff-level AI system design interviews, prompts are intentionally broad (e.g. *"Design an enterprise AI customer support system for 100,000 daily active users"*).

Successful candidates drive the architectural whiteboard structure proactively.

```
1. Scope & Constraints  ──► Clarify QPS (100 QPS), Context Length (4K), Latency SLA (TTFT < 200ms)
2. Back-of-the-Envelope ──► Compute VRAM per node, KV cache footprint, GPU node counts
3. High-Level Blueprint  ──► Gateway -> Semantic Cache -> Hybrid RAG -> vLLM Serving Engine -> Guardrails
4. Technical Deep Dives ──► PagedAttention, Prefix Caching, NLI Guardrails, Disaggregated Prefill
5. Failure & Resiliency ──► Provider fallbacks, circuit breakers, rate limits, PII sanitization
```

### Back-of-the-Envelope Estimation Blueprint

- **Concurrency:** 100 QPS $\times 2000 \text{ tokens/prompt} = 200,000 \text{ active prompt tokens/sec}$.
- **KV Memory:** For 70B model in FP16, KV cache occupies $\approx 1.25 \text{ MB per token}$.
- **GPU Sizing:** 100 active 4K context streams require $\approx 50 \text{ GB}$ VRAM for KV cache alone, requiring dedicated GPU instances (e.g. $8 \times \text{H100}$ node).

## Example

Whiteboard architecture presentation structure:

```markdown
1. API Gateway: Token Bucket Rate Limiter + PII Redaction Proxy + OAuth RBAC.
2. Caching Layer: Redis Semantic Cache (Threshold 0.90 Cosine Similarity).
3. Retrieval Pipeline: Qdrant HNSW Vector Search + BM25 Sparse + Cohere Reranker.
4. Serving Cluster: vLLM Instance with PagedAttention + Chunked Prefill.
5. Observability: OpenTelemetry Tracing + Continuous Ragas Faithfulness Evals.
```

## Interview tips

- Own the whiteboard: lead the conversation smoothly from high-level data flow down to low-level GPU VRAM calculations.
- Always tie technical architecture choices back to business outcomes (SLA latency, token cost, compliance).

## Related Concepts

- [[What is load balancing for LLM inference clusters across multi-region GPU pools?]] (`#151`): [What is load balancing for LLM inference clusters across multi-region GPU pools?](../ai-system-design/what-is-load-balancing-for-llm-inference-clusters-across-multi-region-gpu-pools.md)
- [[How do tensor parallelism (TP) and pipeline parallelism (PP) split large model weights across multi-GPU nodes?]] (`#157`): [How do tensor parallelism (TP) and pipeline parallelism (PP) split large model weights across multi-GPU nodes?](../ai-system-design/how-do-tensor-parallelism-tp-and-pipeline-parallelism-pp-split-large-model-weights-across-multi-gpu-nodes.md)
- [[How to conduct a complete system design interview for a multi-tenant enterprise RAG search platform?]] (`#199`): [How to conduct a complete system design interview for a multi-tenant enterprise RAG search platform?](../interview-experience/how-to-conduct-a-complete-system-design-interview-for-a-multi-tenant-enterprise-rag-search-platform.md)

---

[⬅ Back to Interview Experience](./README.md) · [All topics](../README.md)
