---
title: "How do you build an automated red teaming harness against jailbreaks?"
id: 90
category: "Evaluation and Testing"
difficulty: "Advanced"
tags:
  - ai-engineering
  - evaluation-and-testing
  - interview-questions
---

# How do you build an automated red teaming harness against jailbreaks?

**Short answer:** An automated red teaming harness uses an adversarial attacker LLM to generate diverse prompt injection, jailbreak, and policy-bypassing payloads, firing them automatically at target endpoints and scoring vulnerabilities using specialized safety classifiers.

## Detail

Manual red teaming (security engineers typing jailbreak prompts) is slow and fails to explore the vast combinatorial attack space.

```
[Adversarial Attacker LLM] ──► Generates Jailbreak Variant (e.g. DAN, Base64 encoding)
                                                    │
[Safety Classifier (Llama Guard)] ◄── Target Output ◄── [Target LLM Endpoint]
              │
              ▼
    [Log Vulnerability if Target Bypassed Guardrails]
```

### Automated Red Teaming Workflow

1. **Attacker Mutation Engine:** An attacker LLM takes seed attack prompts and mutates them using techniques like Base64 obfuscation, multi-language translation, role-play framing ("Do Anything Now"), or hypothetical context embedding.
2. **Execution:** Automatically fire hundreds of mutated payloads per minute at target API endpoints.
3. **Automated Vulnerability Scoring:** Pass target model outputs through safety evaluators (Llama Guard / GPT-4 judge) to detect successful safety policy breaches.

## Example

Python concept for an automated red teaming iteration loop:

```python
def run_red_team_attack(attacker_llm, target_endpoint, safety_evaluator, seed_prompt: str):
    # Step 1: Attacker mutates seed jailbreak
    mutation_prompt = f"Rewrite this jailbreak attempt to bypass filters using Base64 framing: '{seed_prompt}'"
    adversarial_payload = attacker_llm.generate(mutation_prompt)
    
    # Step 2: Fire payload at target application
    target_response = target_endpoint.call(adversarial_payload)
    
    # Step 3: Evaluate if safety policy was breached
    is_safe = safety_evaluator.check_safe(target_response)
    if not is_safe:
        print("VULNERABILITY DETECTED! Target bypassed safety guardrails.")
        return {"status": "VULNERABLE", "payload": adversarial_payload, "response": target_response}
    return {"status": "SECURE"}
```

## Interview tips

- Highlight open-source red teaming frameworks like PyRIT (Microsoft) and `promptfoo` redteam.
- Discuss continuously updating seed attack datasets as new jailbreak patterns emerge online.

---

[⬅ Back to Evaluation and Testing](./README.md) · [All topics](../README.md)
