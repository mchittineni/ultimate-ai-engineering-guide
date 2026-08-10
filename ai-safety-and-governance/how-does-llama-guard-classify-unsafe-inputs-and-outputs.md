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

**Short answer:** Llama Guard is a specialized safeguard LLM fine-tuned on safety taxonomies (e.g. MLCommons hazard categories) to evaluate input prompts and output responses in parallel, outputting a structured `safe` or `unsafe` decision along with violated policy category codes.

## Detail

Relying on generic system prompts for safety moderation is unreliable. Llama Guard operates as an independent guardrail model in front of primary LLMs.

### Safety Taxonomy & Hazards

Llama Guard classifies text against explicit risk categories:
- **S1:** Violent Crimes
- **S2:** Non-Violent Crimes
- **S3:** Sex Crimes
- **S4:** Child Exploitation
- **S5:** Suicide / Self-Harm
- **S6:** Cyberattacks / Malware Generation
- **S7:** Chemical / Biological / Nuclear Weapons

### Guardrail Workflow

```
[User Input] ──► [Llama Guard (Input Check)] ──► If "unsafe" ──► Block Request
                         │ If "safe"
                         ▼
                  [Primary LLM] ──► [Llama Guard (Output Check)] ──► If "safe" ──► User
```

Outputs follow a strict format:
- `safe`
- `unsafe\nS6` (indicates violation of Cyberattack category).

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

print(parse_guardrail_response("unsafe\nS6"))
```

## Interview tips

- Highlight latency overhead: running Llama Guard on both input and output adds two model passes; using quantized 8B models on dedicated GPU endpoints minimizes latency impact.
- Compare LLM-based guardrails (Llama Guard) vs rule/regex guardrails (NeMo Guardrails).

---

[⬅ Back to AI Safety and Governance](./README.md) · [All topics](../README.md)
