---
title: "How do you implement distributed tracing for multi-step LLM pipelines?"
id: 8
category: "LLMOps and Production AI"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - llmops-and-production-ai
  - interview-questions
---

# How do you implement distributed tracing for multi-step LLM pipelines?

**Short answer:** Distributed tracing in LLMOps captures nested execution trees (spans) across prompt templates, retrieval steps, vector database queries, tool calls, and model API responses using OpenTelemetry standards (or dedicated platforms like LangSmith/Phoenix) to debug latency, cost, and hallucination bottlenecks.

## Detail

Unlike standard HTTP REST microservices where a request follows a predictable controller-service-database path, LLM pipelines (RAG, ReAct agents, multi-agent frameworks) are non-deterministic and branching.

A single user query might trigger:

1. Query re-writing LLM call ($200$ ms, $150$ tokens)
2. Vector DB hybrid search ($45$ ms, 5 documents)
3. Re-ranker model pass ($80$ ms)
4. Synthesis LLM call ($1800$ ms, $1200$ tokens)

Without structured tracing, diagnosing why a specific user request took 5 seconds or generated inaccurate text requires manual log parsing.

### Core Tracing Primitives

- **Trace:** The overall journey of a single user interaction from input query to final streamed output.
- **Span:** A single unit of work within a trace (e.g., `vector_search`, `llm_generation`, `tool_execution`).
- **Span Attributes:** Metadata attached to each span:
  - Input/Output prompts and tokens.
  - Model parameters (`temperature`, `top_p`).
  - Token counts (`prompt_tokens`, `completion_tokens`).
  - Financial cost ($ USD estimated from token pricing).
  - Error states and exception stack traces.

```text
Trace: User Query ("Summarize Q3 earnings") [Total: 2,125ms | $0.0042]
 ├── Span: embedding_generation [45ms]
 ├── Span: vector_db_retrieve [30ms | 10 docs]
 ├── Span: rerank_documents [50ms | Top 3 retained]
 └── Span: llm_completion [2,000ms | 450 prompt_tokens | 300 completion_tokens]
```

## Example

Implementing OpenTelemetry-compatible tracing using OpenInference and Phoenix / LangSmith abstractions in Python:

```python
from openinference.instrumentation.openai import OpenAIInstrumentor
from opentelemetry import trace as trace_api
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from openai import OpenAI

# 1. Setup OpenTelemetry Tracer
tracer_provider = TracerProvider()
tracer_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
trace_api.set_tracer_provider(tracer_provider)

# 2. Auto-instrument OpenAI Client
OpenAIInstrumentor().instrument()

client = OpenAI()

def run_rag_pipeline(user_query: str):
    tracer = trace_api.get_tracer(__name__)

    with tracer.start_as_current_span("rag_pipeline") as parent_span:
        parent_span.set_attribute("user.query", user_query)

        # Step 1: Retrieval
        with tracer.start_as_current_span("retrieve_context") as retrieve_span:
            retrieved_text = "Q3 Revenue grew by 18% YoY to $4.2 Billion."
            retrieve_span.set_attribute("retrieval.documents_count", 1)

        # Step 2: Generation
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"Context: {retrieved_text}"},
                {"role": "user", "content": user_query}
            ]
        )
        return response.choices[0].message.content

run_rag_pipeline("What was the Q3 revenue growth?")
```

## Interview tips

- Differentiate OpenTelemetry (open standard for tracing traces, metrics, logs) from vendor platforms (LangSmith, Arize Phoenix, Langfuse).
- Explain how sampling strategies (e.g., 100% trace capture for errors/high latency, 5% sample for routine queries) prevent telemetry ingestion costs from exploding in high-throughput environments.

---

[⬅ Back to LLMOps and Production AI](./README.md) · [All topics](../README.md)
