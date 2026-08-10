---
title: "How does Chain-of-Thought (CoT) prompting improve LLM reasoning?"
id: 16
category: "Prompt Engineering"
difficulty: "Beginner"
tags:
  - ai-engineering
  - prompt-engineering
  - interview-questions
---

# How does Chain-of-Thought (CoT) prompting improve LLM reasoning?

**Short answer:** Chain-of-Thought (CoT) prompting guides LLMs to generate explicit intermediate reasoning steps before arriving at a final answer, decomposing complex arithmetic, logic, or symbolic tasks into manageable computational steps.

## Detail

Transformer decoder models generate output auto-regressively token-by-token. If asked to solve a multi-step problem in a single step, the model must compute the final answer in a single forward pass through fixed depth layers.

By prompting the model to produce intermediate text tokens (e.g., *"Let's think step by step"*), the model expands its effective computation time. Each generated intermediate token is re-fed into the context window, allowing subsequent self-attention layers to reference computed intermediate state.

### Variations of CoT

1. **Zero-Shot CoT:** Adding phrases like `"Let's think step by step"` or `"Decompose this problem step by step before answering."`
2. **Few-Shot CoT:** Demonstrating step-by-step reasoning in input-output exemplars.
3. **Structured CoT:** Requiring XML tags like `<thinking>...</thinking>` and `<answer>...</answer>`.

## Example

```python
prompt_standard = "A worker packages 15 boxes an hour. How many boxes in an 8-hour shift with a 30-min break?"

prompt_cot = """A worker packages 15 boxes an hour. How many boxes in an 8-hour shift with a 30-min break?

Let's think step by step:
1. Total shift length = 8 hours.
2. Unpaid break = 30 minutes = 0.5 hours.
3. Total working time = 8 - 0.5 = 7.5 hours.
4. Packaging rate = 15 boxes / hour.
5. Total boxes = 7.5 * 15 = 112.5 -> 112 completed boxes.

Final Answer: 112 boxes."""
```

## Interview tips

- Mention that reasoning models like OpenAI o1/o3 and DeepSeek R1 are explicitly trained via RL to perform internal Chain-of-Thought prior to returning final output tokens.
- Emphasize that while CoT dramatically increases accuracy on math/logic tasks, it increases output token count, increasing latency and API costs.

---

[⬅ Back to Prompt Engineering](./README.md) · [All topics](../README.md)
