---
title: "What is fallback configuration when primary LLM providers return 5xx errors?"
id: 165
category: "LLMOps and Production AI"
difficulty: "Beginner"
tags:
  - ai-engineering
  - llmops-and-production-ai
  - interview-questions
---

# What is fallback configuration when primary LLM providers return 5xx errors?

**Short answer:** Fallback configuration defines automated backup routing rules that automatically redirect active prompt requests to secondary LLM endpoints (e.g. switching from OpenAI to Anthropic or self-hosted vLLM) when primary providers return HTTP 5xx server errors, rate limits, or network timeouts.

## Detail

Third-party API providers experience occasional outages, capacity overloads (503 Service Unavailable), and internal server failures (500 Internal Server Error).

```text
[Incoming User Request] ──► Primary Endpoint (OpenAI GPT-4o) ──► HTTP 503 Outage!
                                                                       │
                                                                       ▼ (Intercept Exception)
                            Secondary Endpoint (Anthropic Claude 3.5) ──► Return Completion
```

### Key Components of Fallback Systems

1. **Retries with Exponential Backoff:** Retrying transient 5xx errors 2–3 times with randomized jitter before failing over.
2. **Provider Agnostic Payloads:** Abstracting request formatting so prompts seamlessly adapt to alternative APIs.
3. **Health Check Probing:** Periodically probing failed primary endpoints to automatically restore primary routing when service recovers.

## Example

Python fallback router snippet:

```python
def execute_with_provider_fallback(prompt: str, primary_provider_fn, fallback_provider_fn) -> str:
    try:
        # Attempt primary provider
        return primary_provider_fn(prompt)
    except Exception as e:
        print(f"Primary Provider Error ({e}). Routing request to Fallback Provider...")
        return fallback_provider_fn(prompt)
```

## Interview tips

- Discuss multi-provider proxy routers like LiteLLM and OpenRouter.
- Highlight format differences across providers (e.g. Anthropic system prompt parameters vs OpenAI system messages).

## Related Concepts

- [[What is graceful degradation in AI services when model providers experience downtime?]] (`#155`): [What is graceful degradation in AI services when model providers experience downtime?](../ai-system-design/what-is-graceful-degradation-in-ai-services-when-model-providers-experience-downtime.md)
- [[How to design an enterprise-grade LLM Gateway with dynamic fallback, tenant rate limiting, and cost allocation?]] (`#169`): [How to design an enterprise-grade LLM Gateway with dynamic fallback, tenant rate limiting, and cost allocation?](../llmops-and-production-ai/how-to-design-an-enterprise-grade-llm-gateway-with-dynamic-fallback-tenant-rate-limiting-and-cost-allocation.md)
- [[How to lead an ambiguous AI system design interview from requirements to architecture?]] (`#196`): [How to lead an ambiguous AI system design interview from requirements to architecture?](../interview-experience/how-to-lead-an-ambiguous-ai-system-design-interview-from-requirements-to-architecture.md)

---

[⬅ Back to LLMOps and Production AI](./README.md) · [All topics](../README.md)
