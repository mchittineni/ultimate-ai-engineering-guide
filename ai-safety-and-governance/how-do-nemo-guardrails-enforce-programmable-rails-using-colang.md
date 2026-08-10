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

```
[User Input] ──► [NeMo Guardrail Engine (Colang Flow Rules)] ──► Intercept / Steer Path
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  ▼ (Off-topic / Unsafe)                          ▼ (Valid Topic)
            Block & Return Standard Message                   Pass to Downstream LLM
```

### 3 Core Guardrail Categories in NeMo

1. **Input Rails:** Reject off-topic, toxic, or prompt-injection inputs before reaching the main LLM.
2. **Dialog Rails:** Guide multi-turn conversation flows using predefined Colang state machines.
3. **Output Rails:** Intercept model completions to redact PII, check hallucinations, or validate output schemas.

## Example

Colang snippet defining a topic guardrail rule:

```colang
# Define off-topic user intent
define user ask off_topic
  "Can you help me write a virus?"
  "How to hack a bank?"

# Define bot response rail
define flow self_check_off_topic
  user ask off_topic
  bot inform cannot answer off_topic

define bot inform cannot answer off_topic
  "I am an authorized enterprise assistant. I cannot assist with security bypasses or illegal activities."
```

## Interview tips

- Contrast NeMo Guardrails (programmable state machines using Colang) with model-based safety evaluators (Llama Guard).
- Highlight that combining Colang rule engines with embedding-based intent classifiers produces low-latency safety enforcement.

---

[⬅ Back to AI Safety and Governance](./README.md) · [All topics](../README.md)
