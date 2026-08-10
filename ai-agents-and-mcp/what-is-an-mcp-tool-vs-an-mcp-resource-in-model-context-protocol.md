---
title: "What is an MCP Tool vs an MCP Resource in Model Context Protocol?"
id: 67
category: "AI Agents and MCP"
difficulty: "Beginner"
tags:
  - ai-engineering
  - ai-agents-and-mcp
  - interview-questions
---

# What is an MCP Tool vs an MCP Resource in Model Context Protocol?

**Short answer:** In the Model Context Protocol (MCP), an MCP Resource is a passive data endpoint that exposes contextual data (files, database tables, logs) for reading, while an MCP Tool is an executable function that performs active operations (writing data, triggering APIs, modifying state).

## Detail

The Anthropic Model Context Protocol (MCP) standardizes how AI applications connect to external data and systems:

| Primitives | Directionality | Mode of Operation | Example |
| --- | --- | --- | --- |
| **MCP Resource** | Read-Only | Passive context reading | Reading a local `schema.sql` file, fetching a log file, reading a git diff |
| **MCP Tool** | Read/Write | Executable action | `send_email()`, `run_git_commit()`, `execute_query()` |
| **MCP Prompt** | Read-Only | Pre-designed template | System prompt templates, workflow guidelines |

### Why Separation Matters

Separating passive resources from executable tools allows clients to enforce fine-grained security policies: resources can be safely auto-read into context, while tools require explicit user confirmation prior to execution.

## Example

JSON-RPC schema difference in MCP:

```json
// MCP Resource Definition (Read Context)
{
  "uri": "file:///logs/app.log",
  "name": "Application Logs",
  "mimeType": "text/plain"
}

// MCP Tool Definition (Executable Action)
{
  "name": "restart_server",
  "description": "Restarts target application container",
  "inputSchema": {
    "type": "object",
    "properties": {
      "server_id": {"type": "string"}
    }
  }
}
```

## Interview tips

- Highlight MCP's architecture: decoupling LLM clients (Claude Desktop, IDEs) from backend data servers via standardized JSON-RPC over stdio or SSE.
- Explain human-in-the-loop security for MCP tool calls.

---

[⬅ Back to AI Agents and MCP](./README.md) · [All topics](../README.md)
