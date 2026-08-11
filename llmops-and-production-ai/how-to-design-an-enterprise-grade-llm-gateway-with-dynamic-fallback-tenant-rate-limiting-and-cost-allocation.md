---
title: "How to design an enterprise-grade LLM Gateway with dynamic fallback, tenant rate limiting, and cost allocation?"
id: 169
category: "LLMOps and Production AI"
difficulty: "Advanced"
tags:
  - ai-engineering
  - llmops-and-production-ai
  - interview-questions
---

# How to design an enterprise-grade LLM Gateway with dynamic fallback, tenant rate limiting, and cost allocation?

**Short answer:** An enterprise-grade LLM Gateway acts as a central proxy architecture providing tenant authentication, dual-metric rate limiting (TPM/RPM via Redis), dynamic provider fallback routing, semantic caching, unified telemetry tracing, and automated billing cost allocation across heterogeneous downstream LLM endpoints.

## Detail

Direct API consumption by internal microservices creates security risks, uncoordinated vendor spend, and rate-limit fragility.

```text
[Internal Microservice A] ──┐
[Internal Microservice B] ──┼──► [Enterprise LLM Gateway Proxy]
[Internal Microservice C] ──┘                 │
                                              ├── [Redis Rate Limiter & Semantic Cache]
                                              ├── [OpenTelemetry Spans + Cost Allocator]
                                              └── [Provider Fallback Engine]
                                                        │
                                     ┌──────────────────┼──────────────────┐
                                     ▼                  ▼                  ▼
                              [OpenAI API]      [Anthropic API]      [vLLM Cluster]
```

### Architectural Sub-Systems

1. **Authentication & Budget Enforcement:** Maps API keys to tenant IDs (`org_sales`) with monthly USD hard caps.
2. **Dual Metric Rate Limiter:** Enforces Requests-Per-Minute (RPM) and Tokens-Per-Minute (TPM) sliding window caps in Redis.
3. **Resilient Provider Router:** Automatically attempts primary model, falling back to secondary providers on HTTP 5xx or rate limits.
4. **Unified Telemetry Logger:** Emits OpenTelemetry spans capturing prompt tokens, completion tokens, latency, and cost.

## Example

Python high-level LLM Gateway proxy middleware:

```python
async def handle_gateway_request(tenant_id: str, request_payload: dict, redis_client, provider_client):
    # 1. Tenant Budget & Rate Limit Check
    if not await check_rate_limit(redis_client, tenant_id, request_payload["estimated_tokens"]):
        return {"error": "HTTP 429: Rate Limit Exceeded"}, 429

    # 2. Semantic Cache Lookup
    cached_resp = await get_semantic_cache(request_payload["prompt"])
    if cached_resp:
        return cached_resp, 200

    # 3. Provider Invocation with Fallback
    response, cost = await provider_client.execute_with_fallback(request_payload)

    # 4. Asynchronous Cost & Metric Logging
    await log_cost_attribution(tenant_id, cost)
    return response, 200
```

## Interview tips

- Discuss OpenTelemetry semantic conventions for AI applications.
- Explain trade-offs between self-building a gateway vs deploying open-source gateways like LiteLLM Proxy.

## Related Concepts

- [[What is document metadata filtering in vector databases?]] (`#123`): [What is document metadata filtering in vector databases?](../rag-and-vector-databases/what-is-document-metadata-filtering-in-vector-databases.md)
- [[What is load balancing for LLM inference clusters across multi-region GPU pools?]] (`#151`): [What is load balancing for LLM inference clusters across multi-region GPU pools?](../ai-system-design/what-is-load-balancing-for-llm-inference-clusters-across-multi-region-gpu-pools.md)
- [[What is cost attribution modeling per user, team, and organization in LLM applications?]] (`#162`): [What is cost attribution modeling per user, team, and organization in LLM applications?](../llmops-and-production-ai/what-is-cost-attribution-modeling-per-user-team-and-organization-in-llm-applications.md)

---

[⬅ Back to LLMOps and Production AI](./README.md) · [All topics](../README.md)
