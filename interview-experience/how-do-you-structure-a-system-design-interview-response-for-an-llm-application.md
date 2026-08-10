---
title: "How do you structure a system design interview response for an LLM application?"
id: 49
category: "Interview Experience"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - interview-experience
  - interview-questions
---

# How do you structure a system design interview response for an LLM application?

**Short answer:** Structure an LLM system design response using a systematic 6-step framework: clarify functional/non-functional requirements (QPS, TTFT, token budgets), calculate scale estimations, design end-to-end data ingest and retrieval pipelines, define model selection and serving infrastructure, detail observability/evals, and address failure modes and security guardrails.

## Detail

LLM system design interviews evaluate both traditional distributed systems principles (load balancing, caching, databases) and AI-specific bottlenecks (VRAM capacity, context windows, token billing).

### The 6-Step LLM System Design Framework

```text
Step 1: Requirements & Scale  ──► Define QPS, TTFT SLA, latency, token limits, accuracy targets
Step 2: High-Level Data Flow  ──► Client -> Proxy -> Cache -> RAG / Agent Loop -> LLM Engine
Step 3: Component Deep-Dive   ──► Vector Indexing (HNSW), Hybrid Search, Reranking, Prompting
Step 4: Inference & Serving   ──► Self-hosted (vLLM/PagedAttention) vs API Provider Routing
Step 5: Evals & Observability ──► OpenTelemetry, Tracing, LLM-as-a-Judge, Regression Testing
Step 6: Reliability & Safety  ──► Guardrails, PII redaction, Rate Limiting, Fallback chains
```

### Scale & Capacity Calculations to Include

- **Concurrency & QPS:** If 10,000 daily active users generate 5 requests/day = 50,000 requests/day $\approx 0.6$ QPS average ($6$ QPS peak).
- **GPU VRAM Estimation:** Model size (70B INT4 $\approx 35\text{ GB}$) + KV Cache per batch stream.

## Example

System design whiteboard component template (Markdown representation):

```text
+------------------+      +-------------------+      +---------------------+
|   Client App     | ---> |  API Gateway /    | ---> |   Semantic Cache    |
| (Web / Mobile)   |      |  Rate Limiter     |      |   (Redis Vector)    |
+------------------+      +-------------------+      +---------------------+
                                   |                            | (Miss)
                                   v                            v
                          +-------------------+      +---------------------+
                          | Input Guardrail   | ---> |  Hybrid Retriever   |
                          | (Llama Guard/PII) |      |  (Qdrant + BM25)    |
                          +-------------------+      +---------------------+
                                                                |
                                                                v
                                                     +---------------------+
                                                     | LLM Serving Engine  |
                                                     | (vLLM / LiteLLM)    |
                                                     +---------------------+
```

## Interview tips

- Proactively state quantitative trade-offs: _"Using a cross-encoder reranker adds ~100ms latency but increases context recall accuracy by 15%."_
- Don't forget guardrails, safety, and evaluation logging when sketching out high-level architectures.

---

[⬅ Back to Interview Experience](./README.md) · [All topics](../README.md)
