---
title: "How does Llama Guard classify unsafe inputs and outputs?"
id: 45
category: "AI Safety and Governance"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - ai-safety-and-governance
  - interview-questions
---

# How does Llama Guard classify unsafe inputs and outputs?

**Short answer:** Llama Guard is a specialized safeguard LLM fine-tuned on safety taxonomies (the MLCommons hazard categories) to classify input prompts and output responses in two separate passes, outputting a structured `safe` or `unsafe` decision along with violated policy category codes.

## Detail

Relying on generic system prompts for safety moderation is unreliable. Llama Guard operates as an independent guardrail model in front of primary LLMs.

### Safety Taxonomy & Hazards

Llama Guard classifies text against the 13 MLCommons hazard categories (Llama Guard 3 adds a 14th). Memorize the codes — interviewers who use these models will know them:

| Code   | Category                  | Code    | Category                               |
| ------ | ------------------------- | ------- | -------------------------------------- |
| **S1** | Violent Crimes            | **S8**  | Intellectual Property                  |
| **S2** | Non-Violent Crimes        | **S9**  | Indiscriminate Weapons (CBRNE)         |
| **S3** | Sex-Related Crimes        | **S10** | Hate                                   |
| **S4** | Child Sexual Exploitation | **S11** | Suicide & Self-Harm                    |
| **S5** | Defamation                | **S12** | Sexual Content                         |
| **S6** | Specialized Advice        | **S13** | Elections                              |
| **S7** | Privacy                   | **S14** | Code Interpreter Abuse (Llama Guard 3) |

### Guardrail Workflow

```text
[User Input] ──► [Llama Guard (Input Check)] ──► If "unsafe" ──► Block Request
                         │ If "safe"
                         ▼
                  [Primary LLM] ──► [Llama Guard (Output Check)] ──► If "safe" ──► User
```

Outputs follow a strict format:

- `safe`
- `unsafe\nS11` (indicates a violation of the Suicide & Self-Harm category).

Note that malware and cyberattack requests are **not** their own category: they fall under S2 (Non-Violent Crimes), with S14 covering abuse of an attached code interpreter.

## Example

Python concept illustrating Llama Guard classification parsing:

```python
def parse_guardrail_response(guard_output: str) -> dict:
    lines = guard_output.strip().splitlines()
    if not lines:
        return {"is_safe": False, "violations": ["UNKNOWN"]}

    status = lines[0].lower()
    if status == "safe":
        return {"is_safe": True, "violations": []}
    else:
        violations = lines[1].split(",") if len(lines) > 1 else ["UNSPECIFIED"]
        return {"is_safe": False, "violations": violations}

print(parse_guardrail_response("unsafe\nS11"))
```

## Interview tips

- Highlight latency overhead: running Llama Guard on both input and output adds two model passes; using quantized 8B models on dedicated GPU endpoints minimizes latency impact.
- Compare LLM-based guardrails (Llama Guard) vs rule/regex guardrails (NeMo Guardrails).

---

[⬅ Back to AI Safety and Governance](./README.md) · [All topics](../README.md)
