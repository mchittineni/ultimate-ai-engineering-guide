---
title: "How does MCP handle streaming updates and progress reporting from long-running tools?"
id: 138
category: "AI Agents and MCP"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - ai-agents-and-mcp
  - interview-questions
---

# How does MCP handle streaming updates and progress reporting from long-running tools?

**Short answer:** Model Context Protocol (MCP) handles streaming updates for long-running tools by issuing JSON-RPC notification messages (`notifications/progress`) over `stdio` or Server-Sent Events (SSE), transmitting progress tokens ($0-100\%$) and incremental status messages to the client host without closing the execution session.

## Detail

Long-running tool tasks (e.g. running an intensive SQL migration or executing a multi-minute build pipeline) cause HTTP timeouts or poor user experience if forced to run synchronously.

```text
MCP Client App ──► JSON-RPC Request `tools/call` (with `progressToken: 42`) ──► MCP Server
                                                                                  │
MCP Client App ◄── Notification `notifications/progress` (progress: 25%) ──────────┤
MCP Client App ◄── Notification `notifications/progress` (progress: 75%) ──────────┤
                                                                                  │
MCP Client App ◄── Final Response Result `jsonrpc: 2.0` (progress: 100%) ─────────┘
```

### Protocol Notification Format

During execution, the MCP server sends non-blocking progress notifications:

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/progress",
  "params": {
    "progressToken": 42,
    "progress": 50,
    "total": 100,
    "message": "Processed 500 / 1000 records"
  }
}
```

## Example

Python concept for sending MCP progress notifications:

```python
import json
import sys

def send_mcp_progress(progress_token: int, current: int, total: int, msg: str):
    notification = {
        "jsonrpc": "2.0",
        "method": "notifications/progress",
        "params": {
            "progressToken": progress_token,
            "progress": current,
            "total": total,
            "message": msg
        }
    }
    # Output notification to stdio transport stream
    sys.stdout.write(json.dumps(notification) + "\n")
    sys.stdout.flush()

send_mcp_progress(progress_token=42, current=50, total=100, msg="Processing batch 5/10...")
```

## Interview tips

- Contrast MCP `stdio` local process streaming with MCP `SSE` remote web socket streaming.
- Highlight how progress reporting improves user experience in IDE assistants (Claude Desktop / VS Code AI extensions).

## Related Concepts

- [[What is synchronous vs asynchronous tool execution in AI agents?]] (`#134`): [What is synchronous vs asynchronous tool execution in AI agents?](../ai-agents-and-mcp/what-is-synchronous-vs-asynchronous-tool-execution-in-ai-agents.md)
- [[What is connection pooling and keep-alive strategy for high-throughput LLM streaming APIs?]] (`#154`): [What is connection pooling and keep-alive strategy for high-throughput LLM streaming APIs?](../ai-system-design/what-is-connection-pooling-and-keep-alive-strategy-for-high-throughput-llm-streaming-apis.md)
- [[How to audit and secure Model Context Protocol (MCP) servers against unauthorized tool invocation?]] (`#190`): [How to audit and secure Model Context Protocol (MCP) servers against unauthorized tool invocation?](../ai-safety-and-governance/how-to-audit-and-secure-model-context-protocol-mcp-servers-against-unauthorized-tool-invocation.md)

---

[⬅ Back to AI Agents and MCP](./README.md) · [All topics](../README.md)
