---
title: "What is the Model Context Protocol (MCP) and how does it work?"
id: 5
category: "AI Agents and MCP"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - ai-agents-and-mcp
  - interview-questions
---

# What is the Model Context Protocol (MCP) and how does it work?

**Short answer:** Model Context Protocol (MCP) is an open standard client-server architecture developed by Anthropic that standardizes how AI applications (clients) connect to external datasets, context sources, and operational tools (servers) over standard JSON-RPC 2.0 transports.

## Detail

Before MCP, connecting AI applications or coding assistants to external systems (e.g., GitHub, Postgres, Jira, Google Drive) required building custom, proprietary integrations for every individual tool and model host. Every new application had to re-implement tool definitions, authentication, and context streaming.

MCP replaces $M \times N$ custom integrations with a clean client-server interface:

````text
┌────────────────────────────────┐
│           MCP Client           │
│   (e.g., Claude Desktop, IDE)  │
└───────────────┬────────────────┘
                │ JSON-RPC 2.0 (stdio / SSE)
                ▼
┌────────────────────────────────┐
│           MCP Server           │
│ (Postgres, GitHub, Slack, etc) │
└────────────────────────────────┘
```text

### Core MCP Primitives

MCP defines three primary capabilities exposed by servers to clients:

1. **Resources:** Read-only data items exposed by the server (e.g., database schemas, file contents, log streams) attached to a URI.
2. **Prompts:** Pre-configured prompt templates and multi-step workflows exposed by the server for standard operations.
3. **Tools:** Executable functions exposed by the server that the LLM can invoke to perform side-effects (e.g., create a GitHub PR, execute a query, post a message).

### Transport Layer

MCP operates over two primary transport channels:

- **`stdio`:** Standard Input/Output communication, ideal for local processes (e.g., local CLI tools, desktop tools).
- **`SSE` (Server-Sent Events) over HTTP:** Used for remote MCP servers running on web servers or cloud endpoints.

## Example

Conceptual implementation of a FastMCP Server in Python:

```python
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server named "DatabaseExplorer"
mcp = FastMCP("DatabaseExplorer")

@mcp.tool()
def execute_sql_query(query: str) -> str:
    """Executes a read-only SQL query against the customer database."""
    # Sanitize and run query
    if "DROP" in query.upper() or "DELETE" in query.upper():
        return "Error: Read-only access permitted."
    return f"Query Results for '{query}': [{'id': 1, 'status': 'active'}]"

@mcp.resource("schema://main")
def get_database_schema() -> str:
    """Exposes database table definitions as a context resource."""
    return "TABLE users (id INT, email VARCHAR, created_at TIMESTAMP);"

if __name__ == "__main__":
    mcp.run(transport="stdio")
```text

## Interview tips

- Emphasize that MCP decouples tool execution from model runtime: the AI host doesn't need to know how to connect to Postgres; it just speaks MCP to the server.
- Mention security & human-in-the-loop: MCP clients act as security boundary enforcement points, prompting the human user to approve destructive tool invocations before sending JSON-RPC execution payloads.

---

[⬅ Back to AI Agents and MCP](./README.md) · [All topics](../README.md)
````
