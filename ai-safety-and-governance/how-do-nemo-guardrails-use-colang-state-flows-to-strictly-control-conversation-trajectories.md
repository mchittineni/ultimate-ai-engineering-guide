---
title: "How do NeMo Guardrails use Colang state flows to strictly control conversation trajectories?"
id: 189
category: "AI Safety and Governance"
difficulty: "Advanced"
tags:
  - ai-engineering
  - ai-safety-and-governance
  - interview-questions
---

# How do NeMo Guardrails use Colang state flows to strictly control conversation trajectories?

**Short answer:** NVIDIA NeMo Guardrails uses Colang, a domain-specific modeling language, to map conversational state transitions into deterministic finite state machines, intercepting user inputs and model outputs to steer dialogue flow, block off-topic queries, and enforce mandatory workflow steps.

## Detail

Natural language prompts cannot guarantee deterministic state transitions in complex multi-step customer support or financial workflows.

NeMo Guardrails acts as a programmable guardrail middleware layer:

```
[User Message] ──► [NeMo Guardrail Engine (Colang Flow Rules)]
                                 │
         ┌───────────────────────┴───────────────────────┐
         ▼ (Off-Topic / Policy Violation)                ▼ (Valid Intent)
   Block & Return Fixed Response                    Forward to Downstream LLM
```

### Colang Structural Elements

1. **User Canonical Forms:** Mapping user phrasing variants to standardized intent tags (`define user ask refund`).
2. **Bot Canonical Forms:** Defining bot response templates (`define bot inform refund_policy`).
3. **Flow Rules:** Explicit state machine logic governing allowed turn sequences.

## Example

Colang script defining an authorized refund workflow:

```colang
define user ask refund
  "I want my money back"
  "Can I get a refund for order 123?"

define flow handle refund request
  user ask refund
  bot ask for order id
  user provide order id
  bot execute tool check_eligibility
  if $eligible == True
    bot inform refund_approved
  else
    bot inform refund_rejected
```

## Interview tips

- Contrast Colang state machines with embedding-based guardrails (Llama Guard): Colang provides deterministic dialog control while embedding classifiers categorize text safety.
- Explain input, output, and dialog guardrail hooks in NeMo.

## Related Concepts

- [[What is an agent state machine and how does state persist across multi-step execution?]] (`#132`): [What is an agent state machine and how does state persist across multi-step execution?](../ai-agents-and-mcp/what-is-an-agent-state-machine-and-how-does-state-persist-across-multi-step-execution.md)
- [[How do DAG-based Multi-Agent Orchestrators prevent state deadlocks?]] (`#139`): [How do DAG-based Multi-Agent Orchestrators prevent state deadlocks?](../ai-agents-and-mcp/how-do-dag-based-multi-agent-orchestrators-prevent-state-deadlocks.md)
- [[How does Llama Guard taxonomy classify unsafe inputs and outputs across safety categories?]] (`#187`): [How does Llama Guard taxonomy classify unsafe inputs and outputs across safety categories?](../ai-safety-and-governance/how-does-llama-guard-taxonomy-classify-unsafe-inputs-and-outputs.md)

---

[⬅ Back to AI Safety and Governance](./README.md) · [All topics](../README.md)
