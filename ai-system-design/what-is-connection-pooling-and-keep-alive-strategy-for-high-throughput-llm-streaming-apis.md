---
title: "What is connection pooling and keep-alive strategy for high-throughput LLM streaming APIs?"
id: 154
category: "AI System Design"
difficulty: "Beginner"
tags:
  - ai-engineering
  - ai-system-design
  - interview-questions
---

# What is connection pooling and keep-alive strategy for high-throughput LLM streaming APIs?

**Short answer:** Connection pooling reuses persistent HTTP/2 or HTTP/1.1 TCP connections (via Keep-Alive headers) between client gateway services and downstream LLM inference endpoints, eliminating TLS handshake latency overhead ($100-300\text{ ms}$) on high-throughput Server-Sent Events (SSE) streaming connections.

## Detail

Opening a new TCP + TLS connection for every incoming LLM prompt request introduces severe latency penalties:

```text
Without Connection Pooling (Per Request):
DNS Lookup ──► TCP 3-Way Handshake ──► TLS 1.3 Handshake (100-300ms Overhead) ──► Send LLM Request

With Connection Pooling (Reused Persistent Socket):
Reused TCP/TLS Socket ──► Immediately Send LLM Request (0ms Connection Overhead!)
```

### Key Infrastructure Configuration Parameters

1. **HTTP/2 Multiplexing:** Transmitting multiple concurrent streaming requests over a single shared TCP connection.
2. **Keep-Alive Timeout:** Maintaining open idle socket connections (e.g. `keepalive_timeout 65s`) to prevent socket churn.
3. **Max Idle Connections Per Host:** Bounding connection pool size to prevent backend socket exhaustion.

## Example

Python `httpx` connection pooling setup for LLM streaming:

```python
import httpx
import asyncio

# Configure persistent connection pool limits
limits = httpx.Limits(max_keepalive_connections=50, max_connections=100, keepalive_expiry=120.0)
client = httpx.AsyncClient(limits=limits, timeout=30.0)

async def stream_llm_completion(prompt: str):
    # Reuses existing pooled TLS connection
    async with client.stream("POST", "https://api.openai.com/v1/chat/completions", json={"model": "gpt-4o-mini"}) as response:
        async for chunk in response.aiter_text():
            pass # Process SSE stream
```

## Interview tips

- Highlight that TLS handshake elimination directly improves Time-to-First-Token (TTFT) SLAs in client applications.
- Discuss socket exhaustion risks (FIN_WAIT_2 / TIME_WAIT states) when connection pools are improperly configured.

## Related Concepts

- [[What is synchronous vs asynchronous tool execution in AI agents?]] (`#134`): [What is synchronous vs asynchronous tool execution in AI agents?](../ai-agents-and-mcp/what-is-synchronous-vs-asynchronous-tool-execution-in-ai-agents.md)
- [[How does MCP handle streaming updates and progress reporting from long-running tools?]] (`#138`): [How does MCP handle streaming updates and progress reporting from long-running tools?](../ai-agents-and-mcp/how-does-mcp-handle-streaming-updates-and-progress-reporting-from-long-running-tools.md)
- [[What is SLA/SLO monitoring for Time-to-First-Token (TTFT) and throughput (Tokens/sec)?]] (`#163`): [What is SLA/SLO monitoring for Time-to-First-Token (TTFT) and throughput (Tokens/sec)?](../llmops-and-production-ai/what-is-sla-slo-monitoring-for-time-to-first-token-ttft-and-throughput-tokens-sec.md)

---

[⬅ Back to AI System Design](./README.md) · [All topics](../README.md)
