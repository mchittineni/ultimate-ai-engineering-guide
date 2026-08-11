---
title: "How do NeMo Guardrails enforce programmable rails using Colang?"
id: 94
category: "AI Safety and Governance"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - ai-safety-and-governance
  - interview-questions
---

# How do NeMo Guardrails enforce programmable rails using Colang?

**Short answer:** NVIDIA NeMo Guardrails uses a domain-specific language called Colang to define programmable flow rules, intercepting LLM interaction steps to steer conversation paths, enforce topic boundaries, block unsafe content, and validate structured JSON outputs.

## Detail

Relying solely on system prompts for safety fails to guarantee strict operational workflows. NeMo Guardrails provides a programmable middleware layer between users and LLMs.

```text
[User Input] ──► [NeMo Guardrail Engine (Colang Flow Rules)] ──► Intercept / Steer Path
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  ▼ (Off-topic / Unsafe)                          ▼ (Valid Topic)
            Block & Return Standard Message                   Pass to Downstream LLM
```

### 5 Rail Types in NeMo

Rails are named by _where in the request lifecycle they fire_, which is the framing to use when asked where a given control belongs:

1. **Input Rails:** Reject off-topic, toxic, or prompt-injection inputs before reaching the main LLM.
2. **Dialog Rails:** Guide multi-turn conversation flows using predefined Colang flows.
3. **Retrieval Rails:** Inspect or filter chunks returned by RAG before they enter the prompt — the hook for indirect prompt injection in retrieved documents.
4. **Execution Rails:** Wrap custom actions/tools, gating what a flow is permitted to invoke.
5. **Output Rails:** Intercept model completions to redact PII, check hallucinations, or validate output schemas.

## Example

Colang snippet defining a topic guardrail rule:

```colang
# Define off-topic user intent
define user ask off_topic
  "Can you help me write a virus?"
  "How to hack a bank?"

# Define the canonical bot response
define bot refuse off_topic
  "I am an authorized enterprise assistant. I cannot assist with security bypasses or illegal activities."

# Wire the intent to the response
define flow handle off_topic
  user ask off_topic
  bot refuse off_topic
```

A note on naming: avoid calling your own flow `self_check_off_topic`. `self check input` and `self check output` are NeMo's _built-in_ rail names, activated from `config.yml` and backed by their own prompt templates — reusing that prefix for a hand-written flow invites confusion about which mechanism is actually running.

```yaml
# config.yml -- built-in rails are enabled here, not in Colang
rails:
  input:
    flows:
      - self check input
  output:
    flows:
      - self check output
```

## Interview tips

- Contrast NeMo Guardrails (programmable flows written in Colang) with model-based safety evaluators (Llama Guard). Note that they compose: a common production setup runs Llama Guard _as_ an input rail.
- Highlight that combining Colang rule engines with embedding-based intent classifiers produces low-latency safety enforcement.
- Know all five rail types and where each fires. "Input and output rails" is the incomplete answer — retrieval and execution rails are where RAG-borne injection and tool abuse get caught.
- For flow mechanics (actions, variable binding, and the limits of Colang's determinism), see [How do NeMo Guardrails use Colang state flows to strictly control conversation trajectories?](./how-do-nemo-guardrails-use-colang-state-flows-to-strictly-control-conversation-trajectories.md) (`#189`).

---

[⬅ Back to AI Safety and Governance](./README.md) · [All topics](../README.md)
