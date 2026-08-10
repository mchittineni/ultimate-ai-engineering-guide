---
title: "How do you implement fallback routing and rate limiting for LLM APIs?"
id: 37
category: "LLMOps and Production AI"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - llmops-and-production-ai
  - interview-questions
---

# How do you implement fallback routing and rate limiting for LLM APIs?

**Short answer:** Production LLM applications protect reliability using proxy routers (e.g. LiteLLM, Portkey) that implement token-bucket rate limiting to prevent HTTP 429 quota errors, alongside cascading fallback routing that automatically fails over across models or providers (e.g. Primary OpenAI GPT-4o $\rightarrow$ Fallback Anthropic Claude 3.5 Sonnet $\rightarrow$ Self-hosted vLLM Llama 3) upon errors or high latency timeouts.

## Detail

Third-party LLM providers frequently suffer rate limits (TPM - Tokens Per Minute, RPM - Requests Per Minute) and temporary service outages.

### Resilience Architecture

```
                                  ┌──► Provider 1 (OpenAI GPT-4o) [Rate Limit Check]
                                  │      │ (HTTP 429 / 5xx Error)
[User App] ──► [LLM Proxy Router] ┼──────┼──► Fallback Provider 2 (Claude 3.5 Sonnet)
                                  │      │ (Timeout)
                                  └──► Fallback Provider 3 (Self-Hosted vLLM)
```

### Key Strategies

1. **Token Bucket Rate Limiting:** Track consumed tokens per user/tenant per minute to smooth out traffic spikes before calling upstream provider APIs.
2. **Exponential Backoff & Jitter:** Automatically retry transient network failures (HTTP 500, 502, 503) with random jitter to prevent thundering herd problems.
3. **Model Fallback Chain:** Define prioritized provider fallback chains matching capabilities (e.g., matching tool calling support).

## Example

Python fallback routing logic using `tenacity` retry library pattern:

```python
import time

def call_llm_with_fallback(prompt: str, providers: list[str]) -> str:
    for provider in providers:
        try:
            print(f"Attempting invocation with provider: {provider}")
            # Simulate API call execution
            if provider == "primary_openai":
                raise Exception("HTTP 429 Rate Limit Exceeded")
            return f"Response from {provider}"
        except Exception as e:
            print(f"Provider {provider} failed: {e}. Cascading to next fallback...")
    raise RuntimeError("All LLM provider fallbacks exhausted.")

result = call_llm_with_fallback("Hello", ["primary_openai", "fallback_anthropic", "self_hosted_vllm"])
print("Result:", result)
```

## Interview tips

- Discuss why naive provider fallbacks can break structured output or tool-calling schemas if fallback models don't support identical JSON schemas.
- Mention cost implications: falling back from a cheaper mini model to a premier model can unexpectedly increase API billing if not monitored.

---

[⬅ Back to LLMOps and Production AI](./README.md) · [All topics](../README.md)
