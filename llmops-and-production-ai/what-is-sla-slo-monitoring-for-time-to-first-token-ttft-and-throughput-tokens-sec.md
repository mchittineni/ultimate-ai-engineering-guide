---
title: "What is SLA/SLO monitoring for Time-to-First-Token (TTFT) and throughput (Tokens/sec)?"
id: 163
category: "LLMOps and Production AI"
difficulty: "Beginner"
tags:
  - ai-engineering
  - llmops-and-production-ai
  - interview-questions
---

# What is SLA/SLO monitoring for Time-to-First-Token (TTFT) and throughput (Tokens/sec)?

**Short answer:** SLA/SLO monitoring tracks key streaming user-experience metrics—Time-to-First-Token (TTFT) measuring initial prompt prefill latency, and Time-Per-Output-Token (TPOT) / Tokens-Per-Second measuring ongoing autoregressive generation throughput—triggering alerts when performance drops below contract SLAs.

## Detail

Traditional REST API SLAs track total request duration. In streaming LLM applications, total request duration depends heavily on requested completion length.

```
Total Request Latency = TTFT (Prefill Delay) + (Generated Tokens * TPOT)
```

### Core Performance Metrics

| Metric | Target SLO Baseline | What it Measures |
| --- | --- | --- |
| **Time-to-First-Token (TTFT)** | $< 200\text{ ms}$ (p95) | Prefill latency before first token streams to user UI |
| **Time-Per-Output-Token (TPOT)** | $< 20\text{ ms}$ (p95) | Latency between consecutive generated tokens |
| **Generation Throughput** | $> 50\text{ tokens/sec}$ | Speed of text generation perceived by end user |

## Example

Python streaming performance profiler:

```python
import time

class LLMStreamProfiler:
    def __init__(self):
        self.start_time = time.time()
        self.first_token_time = None
        self.token_times = []

    def record_token(self):
        now = time.time()
        if self.first_token_time is None:
            self.first_token_time = now
        self.token_times.append(now)

    def get_metrics(self):
        ttft_ms = (self.first_token_time - self.start_time) * 1000.0
        num_tokens = len(self.token_times)
        gen_duration = self.token_times[-1] - self.first_token_time
        tpot_ms = (gen_duration / (num_tokens - 1) * 1000.0) if num_tokens > 1 else 0.0
        throughput = (num_tokens - 1) / gen_duration if gen_duration > 0 else 0.0
        
        return {"ttft_ms": round(ttft_ms, 2), "tpot_ms": round(tpot_ms, 2), "tokens_per_sec": round(throughput, 1)}
```

## Interview tips

- Discuss setting p95 and p99 SLO alerts (e.g. alert on PagerDuty if p95 TTFT exceeds 500ms over a 5-minute window).
- Explain how TTFT vs TPOT disaggregation guides hardware scaling decisions.

## Related Concepts

- [[What is synchronous vs asynchronous tool execution in AI agents?]] (`#134`): [What is synchronous vs asynchronous tool execution in AI agents?](../ai-agents-and-mcp/what-is-synchronous-vs-asynchronous-tool-execution-in-ai-agents.md)
- [[What is connection pooling and keep-alive strategy for high-throughput LLM streaming APIs?]] (`#154`): [What is connection pooling and keep-alive strategy for high-throughput LLM streaming APIs?](../ai-system-design/what-is-connection-pooling-and-keep-alive-strategy-for-high-throughput-llm-streaming-apis.md)
- [[What is structured logging for LLM prompts, completions, and token metrics?]] (`#161`): [What is structured logging for LLM prompts, completions, and token metrics?](../llmops-and-production-ai/what-is-structured-logging-for-llm-prompts-completions-and-token-metrics.md)

---

[⬅ Back to LLMOps and Production AI](./README.md) · [All topics](../README.md)
