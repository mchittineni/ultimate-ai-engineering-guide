---
title: "What is cost attribution modeling per user, team, and organization in LLM applications?"
id: 162
category: "LLMOps and Production AI"
difficulty: "Beginner"
tags:
  - ai-engineering
  - llmops-and-production-ai
  - interview-questions
---

# What is cost attribution modeling per user, team, and organization in LLM applications?

**Short answer:** Cost attribution modeling tracks and calculates exact financial expenditure of LLM API requests per individual user, team, project, or organization tenant by multiplying prompt and completion token counts by provider model pricing tiers.

## Detail

Without cost attribution modeling, shared LLM API accounts present aggregated monthly invoices without visibility into which team or user consumed the budget.

```text
Incoming Request ──► Proxy Gateway ──► Inspect API Key / Tenant Metadata
                                             │
                                             ▼
                                  Execute LLM Completion
                                             │
                                             ▼
              Calculate Cost: (Prompt_Tokens * Price_P + Comp_Tokens * Price_C)
                                             │
                                             ▼
                          Write to Cost Attribution Database
```

### Cost Formula Matrix

$$\text{Cost}_{USD} = \left(\frac{N_{\text{prompt}}}{1000} \times \text{Price}_{\text{prompt}}\right) + \left(\frac{N_{\text{completion}}}{1000} \times \text{Price}_{\text{completion}}\right)$$

Where rates vary significantly by model tier (e.g. GPT-4o vs GPT-4o-mini).

## Example

Python cost calculation engine pattern:

```python
MODEL_PRICING = {
    "gpt-4o": {"prompt": 0.0025, "completion": 0.0100},
    "gpt-4o-mini": {"prompt": 0.00015, "completion": 0.00060},
}

def calculate_request_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    prices = MODEL_PRICING.get(model, {"prompt": 0.002, "completion": 0.006})
    prompt_cost = (prompt_tokens / 1000.0) * prices["prompt"]
    comp_cost = (completion_tokens / 1000.0) * prices["completion"]
    return round(prompt_cost + comp_cost, 6)

cost = calculate_request_cost("gpt-4o", prompt_tokens=1500, completion_tokens=300)
print(f"Calculated Request USD Cost: ${cost:.6f}")
```

## Interview tips

- Discuss setting monthly soft alerts (email notifications at 80% budget) and hard caps (HTTP 429 throttling when 100% budget is reached).
- Connect cost attribution to internal chargeback and showback systems in enterprise engineering organizations.

## Related Concepts

- [[What is an LLM router and how does it dynamically direct queries based on complexity?]] (`#153`): [What is an LLM router and how does it dynamically direct queries based on complexity?](../ai-system-design/what-is-an-llm-router-and-how-does-it-dynamically-direct-queries-based-on-complexity.md)
- [[What is structured logging for LLM prompts, completions, and token metrics?]] (`#161`): [What is structured logging for LLM prompts, completions, and token metrics?](../llmops-and-production-ai/what-is-structured-logging-for-llm-prompts-completions-and-token-metrics.md)
- [[How to design an enterprise-grade LLM Gateway with dynamic fallback, tenant rate limiting, and cost allocation?]] (`#169`): [How to design an enterprise-grade LLM Gateway with dynamic fallback, tenant rate limiting, and cost allocation?](../llmops-and-production-ai/how-to-design-an-enterprise-grade-llm-gateway-with-dynamic-fallback-tenant-rate-limiting-and-cost-allocation.md)

---

[⬅ Back to LLMOps and Production AI](./README.md) · [All topics](../README.md)
