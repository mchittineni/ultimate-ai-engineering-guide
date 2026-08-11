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

**Short answer:** NVIDIA NeMo Guardrails uses Colang, a domain-specific modeling language, to express conversational state transitions as explicit flows, intercepting user inputs and model outputs to steer dialogue, block off-topic queries, and enforce mandatory workflow steps. The _sequencing_ is deterministic; the step that maps a user's utterance onto a canonical form is not.

## Detail

Natural language prompts cannot guarantee reliable state transitions in complex multi-step customer support or financial workflows.

NeMo Guardrails acts as a programmable guardrail middleware layer:

```text
[User Message] ──► [NeMo Guardrail Engine (Colang Flow Rules)]
                                 │
         ┌───────────────────────┴───────────────────────┐
         ▼ (Off-Topic / Policy Violation)                ▼ (Valid Intent)
   Block & Return Fixed Response                    Forward to Downstream LLM
```

### Colang Structural Elements

1. **User Canonical Forms:** Mapping user phrasing variants to standardized intent tags (`define user ask refund`).
2. **Bot Canonical Forms:** Defining bot response templates (`define bot inform refund_policy`).
3. **Flow Rules:** Explicit logic governing allowed turn sequences.
4. **Actions:** Python functions the flow calls with `execute`, binding results into Colang variables.

### Where the Determinism Actually Lives

This is the nuance interviewers dig for, and "Colang gives you a deterministic FSM" is the answer that gets picked apart:

- **Deterministic:** once a turn has been mapped to a canonical form, which flow runs, in what order, and which steps are mandatory. The trajectory is code.
- **Not deterministic:** the mapping itself. NeMo embeds the user's utterance and matches it by vector similarity against the example phrasings under each `define user` block. That is a nearest-neighbour lookup with a threshold — a novel paraphrase can land on the wrong canonical form or none at all, and Colang 1.0 can fall back to asking the LLM to generate a continuation when nothing matches.

So Colang constrains _what may happen next_, not _what the user meant_. Bound the second problem by giving every canonical form enough example utterances, and by defining an explicit fallback flow rather than letting unmatched turns reach a general-purpose LLM.

## Example

Colang script defining an authorized refund workflow:

```colang
define user ask refund
  "I want my money back"
  "Can I get a refund for order 123?"

define user provide order id
  "order 123"
  "it's number 4472"

define flow handle refund request
  user ask refund
  bot ask for order id
  user provide order id
  # `execute` calls a registered Python action and binds its return value.
  # There is no `bot execute tool` form -- actions are flow steps, not bot turns.
  $eligible = execute check_eligibility(order_id=$order_id)
  if $eligible
    bot inform refund_approved
  else
    bot inform refund_rejected

define flow fallback on unmatched intent
  user ...
  bot inform cannot help with that
```

The corresponding action is a plain Python function registered with the rails:

```python
from nemoguardrails.actions import action


@action()
async def check_eligibility(order_id: str) -> bool:
    return await billing.is_refundable(order_id)
```

## Interview tips

- Contrast Colang flows with embedding-based guardrails (Llama Guard): Colang controls dialog _trajectory_ while safety classifiers categorize text _content_. They solve different problems and production systems run both.
- Explain input, output, and dialog guardrail hooks in NeMo.
- Get the `execute` syntax right. Actions bind results into variables (`$x = execute my_action(...)`); writing `bot execute tool ...` signals you have read about Colang but never run it.
- Do not oversell determinism. Say "deterministic flow sequencing over probabilistic intent matching" and you have described the system accurately, including its actual weak point.

## Related Concepts

- [[What is an agent state machine and how does state persist across multi-step execution?]] (`#132`): [What is an agent state machine and how does state persist across multi-step execution?](../ai-agents-and-mcp/what-is-an-agent-state-machine-and-how-does-state-persist-across-multi-step-execution.md)
- [[How do DAG-based Multi-Agent Orchestrators prevent state deadlocks?]] (`#139`): [How do DAG-based Multi-Agent Orchestrators prevent state deadlocks?](../ai-agents-and-mcp/how-do-dag-based-multi-agent-orchestrators-prevent-state-deadlocks.md)
- [[How does Llama Guard taxonomy classify unsafe inputs and outputs across safety categories?]] (`#187`): [How does Llama Guard taxonomy classify unsafe inputs and outputs across safety categories?](../ai-safety-and-governance/how-does-llama-guard-taxonomy-classify-unsafe-inputs-and-outputs-across-safety-categories.md)

---

[⬅ Back to AI Safety and Governance](./README.md) · [All topics](../README.md)
