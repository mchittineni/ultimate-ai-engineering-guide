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

**Short answer:** Llama Guard is a specialized fine-tuned safety classifier model that evaluates user prompts and LLM completions against an explicit safety taxonomy (the MLCommons hazard categories: violent crimes, self-harm, sexual content, privacy, and so on), outputting a binary `safe` or `unsafe` verdict alongside specific category violation codes (e.g. `S1`, `S2`).

## Detail

Instead of relying on rigid keyword lists, Llama Guard processes raw text through a fine-tuned Llama backbone to evaluate nuanced contextual intent.

```text
Input Prompt / Completion Text ──► [Llama Guard Safety Model]
                                          │
                   ┌──────────────────────┴──────────────────────┐
                   ▼ (Safe)                                       ▼ (Unsafe)
               "safe"                                    "unsafe\nS1" (Violent Crimes)
```

### Llama Guard Safety Categories (Taxonomy)

The taxonomy is the 13 MLCommons hazard categories, with Llama Guard 3 adding S14:

- **S1 (Violent Crimes):** Encouraging or detailing physical violence or terrorism.
- **S2 (Non-Violent Crimes):** Financial fraud, property destruction, theft — **and cyber crime such as malware authoring or vulnerability exploitation**.
- **S3 (Sex-Related Crimes):** Sexual assault, trafficking, harassment.
- **S4 (Child Sexual Exploitation):** Child abuse material.
- **S5 (Defamation):** Verifiably false statements that injure a living person's reputation.
- **S6 (Specialized Advice):** Unqualified medical, legal, or financial advice.
- **S7 (Privacy):** Unauthorized disclosure of personal or sensitive information.
- **S8 (Intellectual Property):** Reproducing copyrighted or trademarked material.
- **S9 (Indiscriminate Weapons):** CBRNE and mass-casualty weapon uplift.
- **S10 (Hate):** Demeaning content targeting protected characteristics.
- **S11 (Suicide & Self-Harm):** Encouraging or instructing self-injury.
- **S12 (Sexual Content):** Erotica and explicit sexual material.
- **S13 (Elections):** Disinformation about electoral processes.
- **S14 (Code Interpreter Abuse):** Attempts to escape or weaponize an attached code interpreter (Llama Guard 3 only).

> **Common interview trap:** there is no standalone "cyberattacks" category. Malware and exploitation requests classify as **S2**, not S8 — S8 is Intellectual Property. Getting this backwards is the fastest way to signal you have never actually read a Llama Guard verdict.

### Customizing the Taxonomy Per Deployment

Llama Guard takes the category definitions in its own prompt template, so the taxonomy is configuration rather than a frozen property of the weights:

- **Subset the categories.** Pass only the codes relevant to your product; omitted categories are not evaluated, which cuts false positives (a medical product will usually drop S6 and handle it with a domain policy instead).
- **Rewrite category descriptions.** The natural-language description of each hazard is what the model conditions on, so narrowing S6 to "advice that requires a licensed professional in the user's jurisdiction" is a supported change.
- **Add custom categories.** Append site-specific codes (e.g. `S15: Competitor Disparagement`) with a description in the same format.
- **Condition on role.** The same model scores prompts (`Agent: User`) and completions (`Agent: Assistant`); an output pass sees the full conversation, so a completion can be flagged unsafe even when the prompt that produced it scored safe.

## Example

Python concept illustrating Llama Guard classification parsing:

```python
CATEGORY_NAMES = {
    "S1": "Violent Crimes", "S2": "Non-Violent Crimes", "S3": "Sex-Related Crimes",
    "S4": "Child Sexual Exploitation", "S5": "Defamation", "S6": "Specialized Advice",
    "S7": "Privacy", "S8": "Intellectual Property", "S9": "Indiscriminate Weapons",
    "S10": "Hate", "S11": "Suicide & Self-Harm", "S12": "Sexual Content",
    "S13": "Elections", "S14": "Code Interpreter Abuse",
}


def parse_llama_guard_output(model_raw_output: str) -> dict:
    lines = model_raw_output.strip().splitlines()
    if not lines:
        # Fail closed: an empty verdict is a classifier failure, not an approval.
        return {"is_safe": False, "violations": ["UNKNOWN"]}

    status = lines[0].strip().lower()
    if status == "safe":
        return {"is_safe": True, "violations": []}

    # A verdict can cite several categories on line 2, comma-separated.
    codes = [c.strip() for c in lines[1].split(",")] if len(lines) > 1 else []
    return {
        "is_safe": False,
        "violations": [{"code": c, "name": CATEGORY_NAMES.get(c, "UNKNOWN")} for c in codes]
        or [{"code": "UNSPECIFIED", "name": "UNKNOWN"}],
    }


# A malware-authoring request is S2 (Non-Violent Crimes), NOT a "cyberattack" category.
print(parse_llama_guard_output("unsafe\nS2"))
# {'is_safe': False, 'violations': [{'code': 'S2', 'name': 'Non-Violent Crimes'}]}
```

## Interview tips

- Lead with the customization story: the taxonomy lives in the prompt template, so adding `S15: Competitor Disparagement` or narrowing S6 is a config change, not a fine-tune. That is the answer most candidates miss.
- Contrast running Llama Guard locally on GPU (low latency, high privacy, taxonomy fully under your control) vs third-party Moderation APIs (fixed taxonomy, data egress).
- Know that a category you omit from the prompt is simply not evaluated — trimming the taxonomy cuts false positives but silently removes coverage, so pair it with an eval set per removed category.
- For the raw code table and the input-vs-output guardrail topology, see [How does Llama Guard classify unsafe inputs and outputs?](./how-does-llama-guard-classify-unsafe-inputs-and-outputs.md) (`#45`).

## Related Concepts

- [[What is model jailbreaking and how do safety classifiers block it?]] (`#184`): [What is model jailbreaking and how do safety classifiers block it?](../ai-safety-and-governance/what-is-model-jailbreaking-and-how-do-safety-classifiers-block-it.md)
- [[How to enforce Role-Based Access Control (RBAC) filtering in multi-tenant RAG vector search?]] (`#188`): [How to enforce Role-Based Access Control (RBAC) filtering in multi-tenant RAG vector search?](../ai-safety-and-governance/how-to-enforce-role-based-access-control-rbac-filtering-in-multi-tenant-rag-vector-search.md)
- [[How do NeMo Guardrails use Colang state flows to strictly control conversation trajectories?]] (`#189`): [How do NeMo Guardrails use Colang state flows to strictly control conversation trajectories?](../ai-safety-and-governance/how-do-nemo-guardrails-use-colang-state-flows-to-strictly-control-conversation-trajectories.md)

---

[⬅ Back to AI Safety and Governance](./README.md) · [All topics](../README.md)
