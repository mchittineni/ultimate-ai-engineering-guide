---
title: "What is an OpenTelemetry span in LLM tracing?"
id: 82
category: "LLMOps and Production AI"
difficulty: "Beginner"
tags:
  - ai-engineering
  - llmops-and-production-ai
  - interview-questions
---

# What is an OpenTelemetry span in LLM tracing?

**Short answer:** An OpenTelemetry span represents a single timed operation within a distributed trace (e.g. vector DB lookup, guardrail check, or LLM generation step), recording start/end timestamps, input prompts, output completions, token counts, and error metadata.

## Detail

Complex RAG and agent pipelines consist of multiple chained asynchronous calls. When an agent request takes 4 seconds, raw server logs cannot pinpoint which specific step caused the bottleneck.

```text
[Trace: User Query "Audit Contract"] (Duration: 3.2s)
  ├── Span 1: PII Redaction Guardrail  (Duration: 45ms)
  ├── Span 2: Vector DB Hybrid Search  (Duration: 120ms)
  ├── Span 3: Cohere Reranker          (Duration: 85ms)
  └── Span 4: LLM Generation Step      (Duration: 2950ms) -> Tokens: 450
```

### Key LLM Span Attributes (Semantic Conventions)

- `gen_ai.system`: Provider name (e.g. `openai`, `anthropic`, `vllm`).
- `gen_ai.request.model`: Target model ID (e.g. `gpt-4o`).
- `gen_ai.usage.input_tokens`: Prompt token count.
- `gen_ai.usage.output_tokens`: Completion token count.

## Example

Python manual OpenTelemetry span instrumentation snippet:

```python
from opentelemetry import trace

tracer = trace.get_tracer("llm.pipeline.tracer")

def execute_llm_step(prompt: str):
    with tracer.start_as_current_span("llm_completion_step") as span:
        span.set_attribute("gen_ai.system", "openai")
        span.set_attribute("gen_ai.request.model", "gpt-4o")

        # Simulate LLM call execution
        response_text = "Sample generated completion"

        span.set_attribute("gen_ai.usage.input_tokens", 120)
        span.set_attribute("gen_ai.usage.output_tokens", 45)
        return response_text
```

## Interview tips

- Emphasize standardizing on OpenTelemetry semantic conventions to prevent vendor lock-in across observability platforms (Datadog, Arize, Phoenix, Honeycomb).
- Highlight privacy: redacting sensitive PII from span attribute payloads before emitting traces to external SaaS collectors.

---

[⬅ Back to LLMOps and Production AI](./README.md) · [All topics](../README.md)
