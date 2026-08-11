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

1. **Knowledge Gaps and Out-of-Distribution Prompts:** When asked about facts thinly represented in or absent from pre-training data, the model generates the most plausible-looking completion rather than abstaining. This is the dominant cause.
2. **Training Objectives That Reward Confidence Over Abstention:** Both next-token pre-training and preference tuning reward fluent, committed answers. "I don't know" is rarely the highest-rated response, so models are optimized into confident guessing.
3. **Noisy Pre-Training Data:** Contaminated or contradictory facts in web-scraped corpora.
4. **Attention Degradation:** Context dilution in long prompts ("Lost in the Middle") — grounding is present but not attended to.
5. **Probabilistic Sampling Dynamics:** High temperature or wide sampling distributions draw from lower-probability tail tokens, which _amplifies_ the causes above.

> **Do not claim temperature is the root cause.** Greedy decoding at `T=0` hallucinates freely — a model that does not know a fact has no correct token to rank first, so removing sampling randomness changes nothing about what it does not know. Temperature modulates hallucination rate; knowledge gaps and abstention-averse training create it. Candidates who lead with "just set temperature to 0" get pushed on precisely this.

### Mitigating Hallucinations in Production

- **Retrieval-Augmented Generation (RAG):** Grounding generation in retrieved factual context snippets.
- **Low Temperature Decoding:** Setting $T=0.0$ for factual Q&A. Reduces variance; does not create knowledge.
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

Exact substring matching is illustrative only — it flags any correct claim that has been reworded ("Q3 revenue came to $5.2 million") as a hallucination. Production groundedness checks use NLI entailment models or an LLM judge scoring each extracted claim against its retrieved evidence span, and they report a calibrated score rather than a boolean.

## Interview tips

- Emphasize that LLMs do not "know" facts; they predict tokens. Grounding via RAG or web search is required for accuracy.
- Discuss how RLHF alignment reduces hallucinations but can introduce over-refusal behavior (the alignment tax).

---

[⬅ Back to AI Safety and Governance](./README.md) · [All topics](../README.md)
