---
title: "What is graceful degradation in AI services when model providers experience downtime?"
id: 155
category: "AI System Design"
difficulty: "Beginner"
tags:
  - ai-engineering
  - ai-system-design
  - interview-questions
---

# What is graceful degradation in AI services when model providers experience downtime?

**Short answer:** Graceful degradation is an architectural resilience strategy that maintains core application functionality during external LLM provider outages or rate-limit failures by falling back to secondary model providers, switching to cached responses, disabling optional agent tools, or returning structured static fallback messages.

## Detail

Relying on a single third-party LLM API endpoint creates a single point of failure.

```text
Primary API (OpenAI GPT-4o) ──► HTTP 503 Outage / Timeout
                                        │
                                        ▼
                           [Fallback Router Engine]
                                        │
    ┌───────────────────────────────────┼───────────────────────────────────┐
    ▼ (Option 1)                        ▼ (Option 2)                        ▼ (Option 3)
Route to Anthropic Claude 3.5      Serve Cached Response               Return Deterministic Fallback UI
```

### Key Multi-Tier Degradation Patterns

1. **Provider Fallback Cascade:** Primary (OpenAI) $\to$ Secondary (Anthropic) $\to$ Self-Hosted Open-Source (vLLM Llama 3).
2. **Feature Feature Degradation:** Disabling complex agentic search or web browsing tools while keeping basic Q&A active.
3. **Stale Semantic Cache Serving:** Serving recent cached outputs even if similarity scores fall slightly below strict matching thresholds.

## Example

Python resilient API fallback pattern using `tenacity` retry and fallback:

```python
def call_llm_with_fallback(prompt: str, primary_fn, fallback_fn) -> str:
    try:
        # Attempt primary provider call
        return primary_fn(prompt)
    except Exception as e:
        print(f"Primary Provider Failed ({e}). Initiating graceful degradation fallback...")
        try:
            # Fallback to secondary provider
            return fallback_fn(prompt)
        except Exception as e_fallback:
            print(f"Secondary Provider Failed ({e_fallback}). Returning static response.")
            return "Service is experiencing temporary disruption. Please try again shortly."
```

## Interview tips

- Emphasize cross-provider prompt compatibility: designing prompt templates that work reliably across OpenAI, Anthropic, and open-weight models.
- Discuss Circuit Breaker patterns (Netflix Hystrix pattern applied to LLM proxy routing).

## Related Concepts

- [[What is fallback configuration when primary LLM providers return 5xx errors?]] (`#165`): [What is fallback configuration when primary LLM providers return 5xx errors?](../llmops-and-production-ai/what-is-fallback-configuration-when-primary-llm-providers-return-5xx-errors.md)
- [[How to design an enterprise-grade LLM Gateway with dynamic fallback, tenant rate limiting, and cost allocation?]] (`#169`): [How to design an enterprise-grade LLM Gateway with dynamic fallback, tenant rate limiting, and cost allocation?](../llmops-and-production-ai/how-to-design-an-enterprise-grade-llm-gateway-with-dynamic-fallback-tenant-rate-limiting-and-cost-allocation.md)
- [[How to lead an ambiguous AI system design interview from requirements to architecture?]] (`#196`): [How to lead an ambiguous AI system design interview from requirements to architecture?](../interview-experience/how-to-lead-an-ambiguous-ai-system-design-interview-from-requirements-to-architecture.md)

---

[⬅ Back to AI System Design](./README.md) · [All topics](../README.md)
