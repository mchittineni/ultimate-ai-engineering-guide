---
title: "How do you build a canary deployment pipeline for prompt updates?"
id: 84
category: "LLMOps and Production AI"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - llmops-and-production-ai
  - interview-questions
---

# How do you build a canary deployment pipeline for prompt updates?

**Short answer:** A canary deployment pipeline for prompts routes a small percentage of production user traffic (e.g. 5%) to a newly updated system prompt version, comparing real-time telemetry (user feedback, latency, hallucination evaluation scores) against the baseline version before gradually scaling traffic to 100%.

## Detail

Deploying prompt changes directly to 100% of production users risks widespread quality degradation due to unforeseen edge cases.

```
                  ┌──► 95% Production Traffic ──► Prompt Version 1.0 (Baseline)
[API Gateway] ────┤
                  └──►  5% Canary Traffic     ──► Prompt Version 1.1 (Candidate)
                                                        │
                                                        ▼
                                          [Real-Time Eval Comparison]
                                          If Eval Score Drops -> Auto-Rollback
```

### Deployment Pipeline Stages

1. **Pre-Deployment CI/CD:** Execute golden eval benchmark suite; pass required quality thresholds.
2. **Canary Shift (5%):** Configure API proxy router to assign 5% of incoming user sessions to Prompt `v1.1`.
3. **Real-time Observability Monitoring:** Compare live LLM-as-a-Judge ratings, thumbs up/down rates, and latency.
4. **Automated Rollback / Promotion:** If error rates spike, automatically drop canary traffic to 0%; if metrics remain stable for 2 hours, promote `v1.1` to 100%.

## Example

Python proxy routing logic for canary prompt traffic shifting:

```python
import random

def get_active_prompt_version(tenant_id: str, canary_percentage: float = 0.05) -> str:
    # Deterministic hash or random sampling for canary assignment
    if random.random() < canary_percentage:
        return "prompts/support_v1.1_canary.yaml"
    return "prompts/support_v1.0_baseline.yaml"

prompt_file = get_active_prompt_version("user_123", canary_percentage=0.05)
print("Assigned prompt file:", prompt_file)
```

## Interview tips

- Discuss tenant pinning: ensuring a user assigned to the canary version remains on the same canary version across multi-turn sessions.
- Highlight tracking user-side metrics: thumbs down clicks, user edit rates, and session abandonment.

---

[⬅ Back to LLMOps and Production AI](./README.md) · [All topics](../README.md)
