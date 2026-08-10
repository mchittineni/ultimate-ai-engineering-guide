---
title: "How does MCP server-client architecture standardize context connections?"
id: 69
category: "AI Agents and MCP"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - ai-agents-and-mcp
  - interview-questions
---

# How does MCP server-client architecture standardize context connections?

**Short answer:** The Model Context Protocol (MCP) uses a client-server JSON-RPC 2.0 architecture to decouple AI client applications (e.g. Claude Desktop, IDE extensions) from data integrations (e.g. Postgres, GitHub, Slack), allowing $1$ MCP server implementation to connect universally to any MCP-compliant client.

## Detail

Before MCP, every AI tool integration required custom $M \times N$ integrations between every application host and every external service API.

```text
Legacy:  Host App A ──► Custom Code ──► Postgres
         Host App B ──► Custom Code ──► Postgres

MCP:     Host App A (MCP Client) ──┐
                                   ├── JSON-RPC ──► [Postgres MCP Server]
         Host App B (MCP Client) ──┘
```

### Protocol Mechanics

1. **Transport Layer:** Transport operates over `stdio` (local subprocesses) or Streamable HTTP (remote network services). Streamable HTTP superseded the original standalone HTTP+SSE transport in the 2025-03-26 spec revision; SSE now appears only as an optional upgrade of a `POST` response.
2. **Capability Negotiation:** On connection startup (`initialize`), client and server exchange capabilities (resources, tools, prompts).
3. **JSON-RPC Methods:** Standard methods include `tools/list`, `tools/call`, `resources/read`, and `prompts/get`.

## Example

JSON-RPC 2.0 payload sent by MCP client to execute a tool:

```json
{
  "jsonrpc": "2.0",
  "id": 42,
  "method": "tools/call",
  "params": {
    "name": "query_database",
    "arguments": {
      "sql": "SELECT count(*) FROM users;"
    }
  }
}
```

## Interview tips

- Contrast MCP with traditional OpenAPI custom function calling wrappers: MCP standardizes resource discovery, active tool execution, and prompt templating across vendors.
- Discuss transport security: stdio for local sandboxed tools vs Streamable HTTP over TLS for remote cloud tools, where you must also validate the `Origin` header and bind local servers to localhost to prevent DNS-rebinding attacks.

---

[⬅ Back to AI Agents and MCP](./README.md) · [All topics](../README.md)
