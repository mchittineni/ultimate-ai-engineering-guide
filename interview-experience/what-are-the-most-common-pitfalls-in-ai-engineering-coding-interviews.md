---
title: "What are the most common pitfalls in AI engineering coding interviews?"
id: 96
category: "Interview Experience"
difficulty: "Beginner"
tags:
  - ai-engineering
  - interview-experience
  - interview-questions
---

# What are the most common pitfalls in AI engineering coding interviews?

**Short answer:** The most common pitfalls in AI engineering coding interviews are over-relying on high-level framework wrappers (e.g. LangChain) instead of demonstrating raw Python/SDK mechanics, ignoring API error handling and token limits, failing to handle async streaming, and treating non-deterministic LLMs like traditional deterministic functions.

## Detail

Interviewers evaluate whether candidates understand AI primitives under the hood rather than just gluing together third-party libraries.

### Top 4 Interview Pitfalls

```
1. Framework Wrapper Trap   ──► Calling high-level abstractions without knowing underlying prompt/HTTP payloads
2. Missing Exception Checks ──► Assuming API calls never rate-limit (HTTP 429) or timeout
3. Context Blindness        ──► Passing unlimited text into prompts without calculating token limits
4. Ignoring Streaming       ──► Waiting 10s for full completions instead of returning SSE generators
```

### Best Practices to Stand Out

- **Write Clean SDK / HTTP Code:** Show how to call raw OpenAI / Anthropic SDKs or HTTP endpoints cleanly.
- **Implement Robust Retries:** Wrap external LLM calls with exponential backoff retries.
- **Calculate Token Overhead:** Estimate token counts prior to dispatching prompts.

## Example

Comparing bad vs good interview coding patterns:

```python
# Bad Pattern: No error handling, no token check, naive call
def get_answer_bad(prompt):
    return openai.ChatCompletion.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])

# Good Pattern: Error handling, max token parameter, structured return
def get_answer_good(client, prompt: str, max_tokens: int = 500) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"LLM API Error: {e}")
        return "Fallback: Service temporarily unavailable."
```

## Interview tips

- Ask the interviewer early: *"Would you prefer I use standard Python SDKs or higher-level frameworks like LangChain?"*
- Always talk through trade-offs out loud: cost, latency, context window limits, and model choice.

---

[⬅ Back to Interview Experience](./README.md) · [All topics](../README.md)
