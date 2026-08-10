---
title: "How do you monitor LLM token usage, latency, and costs in production?"
id: 36
category: "LLMOps and Production AI"
difficulty: "Beginner"
tags:
  - ai-engineering
  - llmops-and-production-ai
  - interview-questions
---

# How do you monitor LLM token usage, latency, and costs in production?

**Short answer:** Production LLM monitoring tracks token metrics (prompt vs completion token counts), latency indicators (Time-to-First-Token TTFT and Time-Per-Output-Token TPOT), and API billing metrics using OpenTelemetry instrumentation and dedicated LLM tracing platforms (e.g. LangSmith, Arize Phoenix, Datadog LLM Observability).

## Detail

Unlike traditional microservices where requests take uniform compute, LLM cost and latency scale dynamically with input prompt length and output generation length.

### Core LLM Production Metrics

```
[User Request] ──► [TTFT: Latency to 1st Byte] ──► [TPOT: Decoding Speed] ──► [Total Tokens = Prompt + Completion]
```

1. **Token Metrics:**
   - Prompt Tokens ($T_{in}$): Input token volume (impacts prefill latency and API cost).
   - Completion Tokens ($T_{out}$): Output generated tokens (impacts total generation latency).
2. **Latency Metrics:**
   - **Time-to-First-Token (TTFT):** Time spent processing prompt prefill phase before streaming token 1.
   - **Time-Per-Output-Token (TPOT):** Average inter-token generation time during autoregressive streaming.
3. **Cost Telemetry:**
   - Total Cost ($USD$) = $(T_{in} \times \text{Cost}_{in}) + (T_{out} \times \text{Cost}_{out})$.

## Example

Python Prometheus metric instrumentation for LLM telemetry:

```python
from prometheus_client import Counter, Histogram

LLM_TOKENS_TOTAL = Counter(
    "llm_tokens_total", "Total LLM tokens consumed", ["model", "type"]
)
LLM_LATENCY = Histogram(
    "llm_request_duration_seconds", "LLM request duration", ["model"]
)

def record_llm_metrics(model: str, prompt_tokens: int, completion_tokens: int, duration: float):
    LLM_TOKENS_TOTAL.labels(model=model, type="prompt").inc(prompt_tokens)
    LLM_TOKENS_TOTAL.labels(model=model, type="completion").inc(completion_tokens)
    LLM_LATENCY.labels(model=model).observe(duration)
```

## Interview tips

- Discuss setting up cost anomaly alerts: triggering Slack/pager alerts if token spend spikes unexpectedly due to rogue user loops or prompt injection attacks.
- Explain tenant attribution: tagging requests with `user_id` or `org_id` for enterprise cost chargebacks.

---

[⬅ Back to LLMOps and Production AI](./README.md) · [All topics](../README.md)
