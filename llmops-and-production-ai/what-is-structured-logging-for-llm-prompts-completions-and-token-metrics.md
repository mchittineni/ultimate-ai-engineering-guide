---
title: "What is structured logging for LLM prompts, completions, and token metrics?"
id: 161
category: "LLMOps and Production AI"
difficulty: "Beginner"
tags:
  - ai-engineering
  - llmops-and-production-ai
  - interview-questions
---

# What is structured logging for LLM prompts, completions, and token metrics?

**Short answer:** Structured logging formats LLM interaction payloads into standardized, machine-readable JSON logs capturing prompt inputs, completion text, latency metrics, token consumption counts, provider model IDs, and tenant attribution metadata for downstream analytics and observability pipelines.

## Detail

Unstructured text logging (`print(response)`) makes searching, alerting, and cost accounting impossible across production systems.

```
Unstructured Log: "LLM responded to user 123 in 1.2s with text Hello"

Structured JSON Log:
{
  "timestamp": "2026-08-11T10:30:00Z",
  "trace_id": "tr_99182a",
  "tenant_id": "org_acme",
  "model": "gpt-4o",
  "prompt_tokens": 142,
  "completion_tokens": 38,
  "total_tokens": 180,
  "latency_ms": 1180,
  "cost_usd": 0.0011,
  "status": "success"
}
```

### Essential Log Schema Attributes

1. **Correlation IDs:** `trace_id` and `span_id` mapping multi-step agent trajectories.
2. **Cost Attribution:** `prompt_tokens`, `completion_tokens`, and calculated USD cost.
3. **Quality & Safety Flags:** Guardrail status, latency SLAs, and model temperature settings.

## Example

Python structured logger implementation using standard `logging` and `json`:

```python
import logging
import json
import time

logger = logging.getLogger("llm_observability")

def log_llm_call(trace_id: str, tenant_id: str, model: str, prompt_tokens: int, comp_tokens: int, duration_ms: float):
    log_payload = {
        "event": "llm_completion",
        "trace_id": trace_id,
        "tenant_id": tenant_id,
        "model": model,
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": comp_tokens,
            "total_tokens": prompt_tokens + comp_tokens
        },
        "latency_ms": round(duration_ms, 2)
    }
    logger.info(json.dumps(log_payload))

log_llm_call("trace_881", "tenant_sales", "gpt-4o-mini", 250, 45, 310.5)
```

## Interview tips

- Discuss PII masking in structured logging: redacting sensitive customer data before sending JSON logs to centralized collectors (Datadog/Elasticsearch).
- Highlight log sampling strategies for high-volume production LLM endpoints.

## Related Concepts

- [[What is cost attribution modeling per user, team, and organization in LLM applications?]] (`#162`): [What is cost attribution modeling per user, team, and organization in LLM applications?](../llmops-and-production-ai/what-is-cost-attribution-modeling-per-user-team-and-organization-in-llm-applications.md)
- [[What is SLA/SLO monitoring for Time-to-First-Token (TTFT) and throughput (Tokens/sec)?]] (`#163`): [What is SLA/SLO monitoring for Time-to-First-Token (TTFT) and throughput (Tokens/sec)?](../llmops-and-production-ai/what-is-sla-slo-monitoring-for-time-to-first-token-ttft-and-throughput-tokens-sec.md)
- [[How to handle confidential enterprise telemetry and PII sanitization in compliance-heavy industries?]] (`#170`): [How to handle confidential enterprise telemetry and PII sanitization in compliance-heavy industries?](../llmops-and-production-ai/how-to-handle-confidential-enterprise-telemetry-and-pii-sanitization-in-compliance-heavy-industries.md)

---

[⬅ Back to LLMOps and Production AI](./README.md) · [All topics](../README.md)
