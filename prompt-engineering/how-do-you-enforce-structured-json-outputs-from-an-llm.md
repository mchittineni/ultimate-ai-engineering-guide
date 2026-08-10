---
title: "How do you enforce structured JSON outputs from an LLM?"
id: 17
category: "Prompt Engineering"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - prompt-engineering
  - interview-questions
---

# How do you enforce structured JSON outputs from an LLM?

**Short answer:** Structured JSON outputs can be enforced at the prompt level via schema definitions and Pydantic models, or deterministically at the decoding engine level using context-free grammar (CFG) / JSON Schema constrained decoding (e.g., Outlines, instructor, or vLLM guided decoding).

## Detail

Relying solely on system prompts (e.g., _"Respond in valid JSON"_) fails under edge cases due to token hallucination, missing quotes, or unexpected markdown formatting (` ```json `).

### Enforcement Approaches

1. **Prompt & Pydantic Validation (Retry Loop):** Send JSON schema in system prompt. Parse with Pydantic in a `try-except` block; feed parsing validation errors back to LLM on failure.
2. **Constrained Decoding / Grammars (100% Deterministic):** Libraries like `Outlines`, `lm-format-enforcer`, or vLLM mask invalid logits at decoding time. If the next character must be a quote `"` or colon `:`, non-conforming tokens are set to logit $-\infty$.

## Example

Enforcing structured output using `pydantic` and Instructor / OpenAI structured outputs:

```python
from pydantic import BaseModel, Field

class UserProfile(BaseModel):
    user_id: int
    name: str
    email: str
    roles: list[str] = Field(description="List of assigned RBAC permissions")

# Example JSON schema sent to LLM engine:
schema = UserProfile.model_json_schema()
print("Generated JSON Schema for constrained decoding:\n", schema["properties"])
```

## Interview tips

- Contrast soft prompt instructions vs hard constrained decoding: Constrained decoding guarantees 100% syntactically valid JSON but can slightly alter sampling dynamics if token logits are heavily restricted.
- Explain how structured outputs streamline tool calls and downstream database ingest pipelines in agent workflows.

---

[⬅ Back to Prompt Engineering](./README.md) · [All topics](../README.md)
