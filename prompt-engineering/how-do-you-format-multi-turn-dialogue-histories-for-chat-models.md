---
title: "How do you format multi-turn dialogue histories for chat models?"
id: 114
category: "Prompt Engineering"
difficulty: "Beginner"
tags:
  - ai-engineering
  - prompt-engineering
  - interview-questions
---

# How do you format multi-turn dialogue histories for chat models?

**Short answer:** Multi-turn dialogue histories are formatted as structured arrays of message objects containing standardized role identifiers (`system`, `user`, `assistant`, `tool`), mapped into model-specific chat markup formats (e.g. ChatML tokens `<|im_start|>user...`) via chat templates.

## Detail

LLMs process a single flattened token stream during forward passes. Chat APIs require structured message lists to reconstruct multi-turn conversations cleanly:

```json
[
  {"role": "system", "content": "You are a customer support agent."},
  {"role": "user", "content": "Where is my order?"},
  {"role": "assistant", "content": "Can I have your order ID?"},
  {"role": "user", "content": "Order #12345"}
]
```

### ChatML Token Markup Transformation

The tokenizer converts the JSON message list into special control tokens:

```
<|im_start|>system
You are a customer support agent.<|im_end|>
<|im_start|>user
Where is my order?<|im_end|>
<|im_start|>assistant
Can I have your order ID?<|im_end|>
<|im_start|>user
Order #12345<|im_end|>
<|im_start|>assistant
```

## Example

HuggingFace `apply_chat_template` pattern in Python:

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-7B-Instruct")

messages = [
    {"role": "system", "content": "You are a helpful coding assistant."},
    {"role": "user", "content": "How to sort a list in Python?"},
    {"role": "assistant", "content": "Use `list.sort()` or `sorted()`."},
    {"role": "user", "content": "What is the difference?"}
]

formatted_prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
print("Formatted Chat Template Prompt:\n", formatted_prompt)
```

## Interview tips

- Highlight why manual string concatenation (`"User: ... Assistant: ..."`) causes unexpected output degradation compared to using native tokenizer chat templates.
- Discuss managing multi-turn context limits via sliding-window history or chat message summarization.

## Related Concepts

- [[What is an agent state machine and how does state persist across multi-step execution?]] (`#132`): [What is an agent state machine and how does state persist across multi-step execution?](../ai-agents-and-mcp/what-is-an-agent-state-machine-and-how-does-state-persist-across-multi-step-execution.md)
- [[How does MCP handle streaming updates and progress reporting from long-running tools?]] (`#138`): [How does MCP handle streaming updates and progress reporting from long-running tools?](../ai-agents-and-mcp/how-does-mcp-handle-streaming-updates-and-progress-reporting-from-long-running-tools.md)
- [[What is connection pooling and keep-alive strategy for high-throughput LLM streaming APIs?]] (`#154`): [What is connection pooling and keep-alive strategy for high-throughput LLM streaming APIs?](../ai-system-design/what-is-connection-pooling-and-keep-alive-strategy-for-high-throughput-llm-streaming-apis.md)

---

[⬅ Back to Prompt Engineering](./README.md) · [All topics](../README.md)
