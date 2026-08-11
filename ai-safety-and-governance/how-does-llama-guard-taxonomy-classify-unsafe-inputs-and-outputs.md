---
title: "How does Llama Guard taxonomy classify unsafe inputs and outputs across safety categories?"
id: 187
category: "AI Safety and Governance"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - ai-safety-and-governance
  - interview-questions
---

# How does Llama Guard taxonomy classify unsafe inputs and outputs across safety categories?

**Short answer:** Llama Guard is a specialized fine-tuned safety classifier model that evaluates user prompts and LLM completions against an explicit safety taxonomy (e.g. violent crimes, self-harm, cyberattacks, sexual content), outputting a binary `safe` or `unsafe` verdict alongside specific category violation codes (e.g. `S1`, `S2`).

## Detail

Instead of relying on rigid keyword lists, Llama Guard processes raw text through a fine-tuned Llama backbone to evaluate nuanced contextual intent.

```
Input Prompt / Completion Text ──► [Llama Guard Safety Model]
                                          │
                   ┌──────────────────────┴──────────────────────┐
                   ▼ (Safe)                                       ▼ (Unsafe)
               "safe"                                    "unsafe\nS1" (Violent Crimes)
```

### Llama Guard Safety Categories (Taxonomy)

- **S1 (Violent Crimes):** Encouraging or detailing physical violence or terrorism.
- **S2 (Non-Violent Crimes):** Financial fraud, property destruction, theft.
- **S3 (Sex-Related Crimes):** Sexual assault, exploitation.
- **S4 (Child Exploitation):** Child abuse material.
- **S5 (Defamation / Hate):** Hate speech, harassment.
- **S6 (Specialized Advice):** Unqualified medical, legal, or financial advice.
- **S7 (Privacy / PII):** Unauthorized disclosure of personal secrets.
- **S8 (Cyberattacks):** Malware creation, vulnerability exploitation.

## Example

Python concept illustrating Llama Guard classification parsing:

```python
def parse_llama_guard_output(model_raw_output: str) -> dict:
    lines = model_raw_output.strip().splitlines()
    if not lines:
        return {"is_safe": False, "violation": "UNKNOWN"}
        
    status = lines[0].lower()
    if status == "safe":
        return {"is_safe": True, "violation": None}
    else:
        violation_code = lines[1] if len(lines) > 1 else "UNSPECIFIED"
        return {"is_safe": False, "violation": violation_code}

print(parse_llama_guard_output("unsafe\nS8"))
```

## Interview tips

- Highlight that Llama Guard supports prompt-level taxonomy customization: developers can add or remove safety categories directly in the system prompt.
- Contrast running Llama Guard locally on GPU (low latency, high privacy) vs third-party Moderation APIs.

## Related Concepts

- [[What is model jailbreaking and how do safety classifiers block it?]] (`#184`): [What is model jailbreaking and how do safety classifiers block it?](../ai-safety-and-governance/what-is-model-jailbreaking-and-how-do-safety-classifiers-block-it.md)
- [[How to enforce Role-Based Access Control (RBAC) filtering in multi-tenant RAG vector search?]] (`#188`): [How to enforce Role-Based Access Control (RBAC) filtering in multi-tenant RAG vector search?](../ai-safety-and-governance/how-to-enforce-role-based-access-control-rbac-filtering-in-multi-tenant-rag-vector-search.md)
- [[How do NeMo Guardrails use Colang state flows to strictly control conversation trajectories?]] (`#189`): [How do NeMo Guardrails use Colang state flows to strictly control conversation trajectories?](../ai-safety-and-governance/how-do-nemo-guardrails-use-colang-state-flows-to-strictly-control-conversation-trajectories.md)

---

[⬅ Back to AI Safety and Governance](./README.md) · [All topics](../README.md)
