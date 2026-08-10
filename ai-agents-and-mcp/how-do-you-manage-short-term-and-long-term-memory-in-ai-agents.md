---
title: "How do you manage short-term and long-term memory in AI agents?"
id: 25
category: "AI Agents and MCP"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - ai-agents-and-mcp
  - interview-questions
---

# How do you manage short-term and long-term memory in AI agents?

**Short answer:** Short-term memory manages active conversation state within the LLM's finite context window using sliding windows, message truncation, or iterative summarization; long-term memory persists facts, preferences, and previous agent execution outcomes across sessions using vector databases (semantic recall) and key-value/graph stores.

## Detail

Agent memory systems mirror human memory cognitive architectures:

```
[Agent Perception]
       │
       ├──► Short-Term Memory ──► Sliding Window / Context Buffer (In-Memory)
       │
       └──► Long-Term Memory  ──► Vector Search (Episodic) + Knowledge Graph (Semantic)
```

| Memory Type | Technology | Purpose | Eviction / Compression Strategy |
| --- | --- | --- | --- |
| **Short-Term (Working)** | Context window (Message array) | Maintaining current conversation goal & multi-turn tool logs | Sliding window, message trimming, LLM conversation summarization |
| **Long-Term Episodic** | Vector Database (Embeddings) | Recalling past user sessions, past agent task executions | Semantic similarity retrieval ($k$-NN search) |
| **Long-Term Procedural** | Key-Value / Graph DB / SQL | Storing explicit user profiles, entities, system rules | CRUD database operations |

### Context Window Optimization

To prevent context window overflow during long agent sessions:
1. **Windowed Buffer:** Retain only the last $N$ turns.
2. **Summary Buffer:** When message history exceeds token threshold (e.g., 8,000 tokens), compress older turns into a high-level summary using a background LLM pass.

## Example

Python conceptual representation of memory management:

```python
class AgentMemory:
    def __init__(self, token_limit: int = 4000):
        self.short_term = [] # active turns
        self.token_limit = token_limit

    def add_turn(self, role: str, content: str):
        self.short_term.append({"role": role, "content": content})
        self._check_and_compress()

    def _check_and_compress(self):
        # Calculate total tokens (estimated)
        total_tokens = sum(len(m["content"].split()) * 1.3 for m in self.short_term)
        if total_tokens > self.token_limit:
            # Compress oldest 50% into a single system summary turn
            old_turns = self.short_term[:len(self.short_term)//2]
            summary_text = f"Summary of past interactions: {len(old_turns)} turns compressed."
            self.short_term = [{"role": "system", "content": summary_text}] + self.short_term[len(self.short_term)//2:]
```

## Interview tips

- Discuss how frameworks like MemGPT (Letta) manage RAM (context window) vs Disk (external DB) using explicit OS-like paging instructions (`core_memory_append`, `archival_memory_search`).
- Mention privacy and compliance (GDPR) requirements when persisting long-term user memories.

---

[⬅ Back to AI Agents and MCP](./README.md) · [All topics](../README.md)
