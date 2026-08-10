---
title: "How do you design a multi-tenant LLM gateway with rate limits?"
id: 79
category: "AI System Design"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - ai-system-design
  - interview-questions
---

# How do you design a multi-tenant LLM gateway with rate limits?

**Short answer:** A multi-tenant LLM gateway acts as a centralized proxy service that handles authentication, tenant tier rate limiting (Tokens-Per-Minute TPM and Requests-Per-Minute RPM using Redis token buckets), request routing, token usage tracking, and provider fallback management across downstream LLM endpoints.

## Detail

Directly exposing vendor LLM API keys to internal microservices or client apps creates security, cost, and rate-limit compliance risks.

```
[Client Tenant A] ──┐
                    ├──► [LLM Gateway Proxy (LiteLLM / Custom)] ──► [Redis Rate Limiter]
[Client Tenant B] ──┘         │                                         │
                              ▼                                         ▼
                     (Provider Routing) ───────────► [OpenAI / Anthropic / vLLM]
```

### Core Gateway Components

1. **Tenant Authentication & Authorization:** API keys map to tenant IDs (`org_123`) and billing tiers.
2. **Dual-Metric Rate Limiting:**
   - **Requests-Per-Minute (RPM):** Prevents connection starvation.
   - **Tokens-Per-Minute (TPM):** Tracks estimated prompt + max completion tokens using Leaky Bucket / Token Bucket algorithms.
3. **Usage Attribution Log:** Emits OpenTelemetry metrics recording `tenant_id`, `prompt_tokens`, `completion_tokens`, and cost.

## Example

Redis token-bucket rate limiter pattern in Python:

```python
import time

def check_tenant_tpm_limit(redis_client, tenant_id: str, estimated_tokens: int, tpm_limit: int = 100000) -> bool:
    current_minute = int(time.time() // 60)
    key = f"rate_limit:{tenant_id}:{current_minute}"
    
    # Pipeline increment and expiry setting
    current_usage = redis_client.incrby(key, estimated_tokens)
    if current_usage == estimated_tokens:
        redis_client.expire(key, 120)
        
    if current_usage > tpm_limit:
        return False # Rate limit exceeded (HTTP 429)
    return True
```

## Interview tips

- Discuss prompt token estimation prior to LLM invocation (using fast local tokenizers like `tiktoken` to estimate input token volume for rate limits).
- Explain handling upstream HTTP 429 rate limit responses gracefully via exponential backoff with jitter.

---

[⬅ Back to AI System Design](./README.md) · [All topics](../README.md)
