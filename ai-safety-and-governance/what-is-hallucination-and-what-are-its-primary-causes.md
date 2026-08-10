---
title: "What is hallucination and what are its primary causes?"
id: 93
category: "AI Safety and Governance"
difficulty: "Beginner"
tags:
  - ai-engineering
  - ai-safety-and-governance
  - interview-questions
---

# What is hallucination and what are its primary causes?

**Short answer:** Hallucination in LLMs refers to the generation of plausible-sounding but factually incorrect, ungrounded, or nonsensical output text; it is primarily caused by probabilistic next-token sampling, out-of-distribution prompts, noisy pre-training data, and attention degradation over long contexts.

## Detail

LLMs are probabilistic token predictors, not factual search engines. Models calculate next-token likelihoods based on statistical pattern associations.

### Primary Root Causes

1. **Probabilistic Sampling Dynamics:** High temperature ($T > 0.8$) or wide sampling distributions encourage sampling from lower-probability tail tokens.
2. **Out-of-Distribution (OOD) Knowledge Cutoffs:** When asked about facts outside pre-training data, the model attempts to generate plausible completions matching prompt syntax rather than admitting ignorance.
3. **Noisy Pre-Training Data:** Contaminated or contradictory facts in web-scraped corpora.
4. **Attention Degradation:** Context dilution in long prompts ("Lost in the Middle").

### Mitigating Hallucinations in Production

- **Retrieval-Augmented Generation (RAG):** Grounding generation in retrieved factual context snippets.
- **Low Temperature Decoding:** Setting $T=0.0$ for factual Q&A.
- **Constrained Decoding & Guardrails:** Validating outputs against external fact databases or schemas.

## Example

Python concept measuring claim verification against ground truth:

```python
def check_hallucination_claim(generated_claim: str, verified_facts: list[str]) -> bool:
    # If generated claim does not match any verified ground truth fact -> flag hallucination
    is_grounded = any(fact in generated_claim for fact in verified_facts)
    return not is_grounded # Returns True if hallucinated

facts = ["Revenue for Q3 was $5.2M"]
generated_output = "Revenue for Q3 was $9.8M"

print("Is Hallucinated:", check_hallucination_claim(generated_output, facts))
```

## Interview tips

- Emphasize that LLMs do not "know" facts; they predict tokens. Grounding via RAG or web search is required for accuracy.
- Discuss how RLHF alignment reduces hallucinations but can introduce over-refusal behavior (the alignment tax).

---

[⬅ Back to AI Safety and Governance](./README.md) · [All topics](../README.md)
