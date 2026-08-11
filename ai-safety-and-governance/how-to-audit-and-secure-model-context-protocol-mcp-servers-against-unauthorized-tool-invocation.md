---
title: "How to audit and secure Model Context Protocol (MCP) servers against unauthorized tool invocation?"
id: 190
category: "AI Safety and Governance"
difficulty: "Advanced"
tags:
  - ai-engineering
  - ai-safety-and-governance
  - interview-questions
---

# How to audit and secure Model Context Protocol (MCP) servers against unauthorized tool invocation?

**Short answer:** Securing Model Context Protocol (MCP) servers requires enforcing mutual authentication (OAuth 2.0 / TLS for SSE transport), schema validation on all tool arguments, role-based tool permission scoping, explicit human approval (HITL) checkpoints before executing state-modifying tools, and structured JSON-RPC audit logging.

## Detail

The Model Context Protocol (MCP) standardizes how AI applications invoke tools and read resources.

If an MCP server exposes powerful tools (e.g. `drop_database` or `send_email`) without strict security, an indirect prompt injection attack can hijack the AI client into triggering destructive actions.

```
AI Client (Claude / IDE) ──► JSON-RPC over stdio/SSE ──► [MCP Security Middleware Layer]
                                                                  │
                    ┌─────────────────────────────────────────────┴─────────────────────────────────────────────┐
                    ▼ (Tool: Read-only `read_file`)                                                             ▼ (Tool: Destructive `delete_db`)
             Execute Safely                                                                             Require Human Approval Token
```

### Security Layers for MCP Servers

1. **Tool Permission Scoping:** Restricting MCP servers to minimal necessary privileges (Least Privilege Principle).
2. **Schema & Argument Sanitization:** Using Pydantic validators on incoming JSON-RPC `params.arguments`.
3. **Transport Layer Security:** Running local subprocess tools over sandboxed `stdio`, and securing remote SSE endpoints with TLS and bearer tokens.

## Example

Python MCP tool security wrapper snippet:

```python
def mcp_secure_tool_wrapper(tool_name: str, args: dict, user_role: str, execute_fn):
    READ_ONLY_TOOLS = {"read_resource", "list_tables", "get_status"}
    
    if tool_name not in READ_ONLY_TOOLS and user_role != "admin":
        raise PermissionError(f"MCP Security Error: Role '{user_role}' unauthorized to call tool '{tool_name}'.")
        
    return execute_fn(args)
```

## Interview tips

- Highlight MCP's explicit distinction between passive read-only **Resources** and active executable **Tools**.
- Discuss auditing JSON-RPC notification streams for unusual tool invocation patterns.

## Related Concepts

- [[What is an agent tool schema and how do parameters get validated before invocation?]] (`#131`): [What is an agent tool schema and how do parameters get validated before invocation?](../ai-agents-and-mcp/what-is-an-agent-tool-schema-and-how-do-parameters-get-validated-before-invocation.md)
- [[How does MCP handle streaming updates and progress reporting from long-running tools?]] (`#138`): [How does MCP handle streaming updates and progress reporting from long-running tools?](../ai-agents-and-mcp/how-does-mcp-handle-streaming-updates-and-progress-reporting-from-long-running-tools.md)
- [[How do sandbox execution environments secure Code Interpreter tools?]] (`#140`): [How do sandbox execution environments secure Code Interpreter tools?](../ai-agents-and-mcp/how-do-sandbox-execution-environments-secure-code-interpreter-tools.md)

---

[⬅ Back to AI Safety and Governance](./README.md) · [All topics](../README.md)
