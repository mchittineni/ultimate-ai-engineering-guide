---
title: "How to prepare for an AI Engineer coding interview (raw SDK vs frameworks)?"
id: 191
category: "Interview Experience"
difficulty: "Beginner"
tags:
  - ai-engineering
  - interview-experience
  - interview-questions
---

# How to prepare for an AI Engineer coding interview (raw SDK vs frameworks)?

**Short answer:** Prepare for AI Engineer coding interviews by mastering standard Python, async streaming, Pydantic schema validation, and raw model provider SDKs (OpenAI / Anthropic) rather than relying on high-level framework wrappers (like LangChain); interviewers value candidates who understand raw HTTP payloads, prompt formatting mechanics, and error handling.

## Detail

Interviewers evaluate whether candidates understand core AI primitives under the hood.

```text
Framework Wrapper Trap:  `agent.run("Do task")` ──► Obscures underlying API calls, prompts, and retries.
Production AI Engineer: Raw SDK / HTTP calls + Pydantic validation + `asyncio` streaming + Exponential backoff.
```

### 4 Core Technical Skills Interviewers Probe

1. **Structured Outputs:** Using Pydantic models with `response_format` or function calling schemas.
2. **Streaming & Async I/O:** Handling Server-Sent Events (SSE) using `asyncio` and `httpx`.
3. **Resilient Error Handling:** Implementing retries for rate limits (HTTP 429) and timeouts.
4. **Token Management:** Calculating token lengths locally using `tiktoken`.

## Example

Clean raw SDK coding pattern preferred in technical interviews:

```python
import asyncio
from openai import AsyncOpenAI
from pydantic import BaseModel

class CodeAnalysis(BaseModel):
    has_bugs: bool
    summary: str

client = AsyncOpenAI()

async def analyze_code_clean(code_snippet: str) -> CodeAnalysis:
    # Use native structured output parsing
    completion = await client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a Python code reviewer."},
            {"role": "user", "content": f"Analyze: {code_snippet}"}
        ],
        response_format=CodeAnalysis
    )
    return completion.choices[0].message.parsed
```

## Interview tips

- Ask the interviewer early: _"Would you prefer I use official provider SDKs or higher-level frameworks?"_
- Always talk through trade-offs out loud: cost, latency, token limits, and fallback strategies.

## Related Concepts

- [[What is prompt priming and how does it set expectations for LLM responses?]] (`#111`): [What is prompt priming and how does it set expectations for LLM responses?](../prompt-engineering/what-is-prompt-priming-and-how-does-it-set-expectations-for-llm-responses.md)
- [[What is an agent system prompt and how does it define tool availability?]] (`#135`): [What is an agent system prompt and how does it define tool availability?](../ai-agents-and-mcp/what-is-an-agent-system-prompt-and-how-does-it-define-tool-availability.md)
- [[How to handle live coding failures and non-deterministic model outputs during interviews?]] (`#197`): [How to handle live coding failures and non-deterministic model outputs during interviews?](../interview-experience/how-to-handle-live-coding-failures-and-non-deterministic-model-outputs-during-interviews.md)

---

[⬅ Back to Interview Experience](./README.md) · [All topics](../README.md)
