---
title: "How do you budget and cap monthly LLM API costs?"
id: 83
category: "LLMOps and Production AI"
difficulty: "Beginner"
tags:
  - ai-engineering
  - llmops-and-production-ai
  - interview-questions
---

# How do you budget and cap monthly LLM API costs?

**Short answer:** Monthly LLM API costs are budgeted and capped by enforcing per-tenant token usage quotas, deploying cost attribution proxy routers (e.g. LiteLLM), setting automated soft/hard billing alerts, implementing semantic caching to prevent redundant calls, and routing low-complexity tasks to smaller models.

## Detail

Uncapped LLM API usage poses severe financial risks: a single infinite loop in an agent script or a recursive prompt injection attack can generate thousands of dollars in token billing overnight.

```text
[User App] ──► [Proxy Router (LiteLLM)] ──► Check Monthly Tenant Spend
                                                   │
                   ┌───────────────────────────────┴───────────────────────────────┐
                   ▼ (Spend < $500 Budget)                                         ▼ (Spend >= $500 Budget)
            Allow Request                                                Reject HTTP 429 / Cut Off
```

### Cost Governance Controls

1. **Per-Tenant Hard Caps:** Set maximum monthly USD billing limits per API key/tenant.
2. **Model Tier Routing:** Reserve frontier reasoning models for tasks that need them; route routine classification and extraction to a small/cheap tier or a self-hosted open model. Quote current per-million-token rates from the provider's pricing page rather than from memory — they move often, and vendor model names churn faster still.
3. **Max Completion Token Caps:** Always set `max_tokens` parameters on API invocations to prevent run-away generations.

## Example

Python budget tracking logic snippet:

```python
class BudgetTracker:
    def __init__(self, monthly_budget_usd: float = 500.0):
        self.monthly_budget = monthly_budget_usd
        self.current_spend = 0.0

    def check_and_track(
        self,
        prompt_tokens: int,
        completion_tokens: int,
        # Pass live rates from a config file, per model. Hardcoded defaults go
        # stale fast and silently misreport spend once prices move.
        cost_per_1m_prompt: float,
        cost_per_1m_comp: float,
    ) -> bool:
        call_cost = ((prompt_tokens / 1_000_000) * cost_per_1m_prompt) + (
            (completion_tokens / 1_000_000) * cost_per_1m_comp
        )
        if self.current_spend + call_cost > self.monthly_budget:
            raise RuntimeError(f"Monthly budget limit of ${self.monthly_budget} exceeded. Request blocked.")

        self.current_spend += call_cost
        return True
```

## Interview tips

- Discuss setting soft alert thresholds (e.g. email alert when hitting 80% of budget cap).
- Highlight that semantic caching saves you exactly its hit rate, so cite the measured hit rate for your traffic rather than a generic percentage.

---

[⬅ Back to LLMOps and Production AI](./README.md) · [All topics](../README.md)
