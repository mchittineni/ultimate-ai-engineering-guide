---
title: "What is negative prompting and how do you instruct models what not to do?"
id: 112
category: "Prompt Engineering"
difficulty: "Beginner"
tags:
  - ai-engineering
  - prompt-engineering
  - interview-questions
---

# What is negative prompting and how do you instruct models what not to do?

**Short answer:** Negative prompting explicitly specifies prohibited behaviors, restricted topics, or disallowed words, preventing model hallucinations, off-topic rambling, and safety policy breaches.

## Detail

LLMs process text by predicting tokens that align with prompt semantics. Naive negative instructions like _"Do NOT think of a pink elephant"_ often inadvertently increase attention weight on the banned concept.

```text
Weak Negative Prompt:   "Don't generate conversational intros." (Model often outputs "Sure! Here is...")
Strong Negative Prompt: "Respond strictly with the target JSON object. Zero conversational filler or introductory text."
```

### Best Practices for Negative Directives

1. **Positive Replacement:** Instead of solely banning a behavior, instruct the model on the positive alternative (e.g. _"Instead of bullet points, use a single continuous paragraph"_).
2. **XML Tag Isolation:** Wrap negative rules inside distinct structural blocks (`<disallowed_actions>`).
3. **Structured Validation Guardrails:** Pair negative prompts with Pydantic output validation to catch edge-case violations.

## Example

Python prompt comparison highlighting positive framing of negative constraints:

```python
# Weak
prompt_weak = "Write a summary. Do not include pricing or competitor names."

# Strong
prompt_strong = """Write a product summary.
DISALLOWED:
- Do NOT mention pricing or competitor brand names.

REQUIRED FORMAT:
- Focus exclusively on technical product specifications and core features."""
```

## Interview tips

- Explain why LLMs sometimes ignore negative constraints (due to token-level self-attention activating mentioned concepts).
- Mention combining negative prompts with output guardrail classifiers like Llama Guard or regex validators.

## Related Concepts

- [[What is model jailbreaking and how do safety classifiers block it?]] (`#184`): [What is model jailbreaking and how do safety classifiers block it?](../ai-safety-and-governance/what-is-model-jailbreaking-and-how-do-safety-classifiers-block-it.md)
- [[What is assertion testing in LLM unit tests?]] (`#173`): [What is assertion testing in LLM unit tests?](../evaluation-and-testing/what-is-assertion-testing-in-llm-unit-tests.md)
- [[How to explain LLM hallucination mitigation in a system design interview?]] (`#195`): [How to explain LLM hallucination mitigation in a system design interview?](../interview-experience/how-to-explain-llm-hallucination-mitigation-in-a-system-design-interview.md)

---

[⬅ Back to Prompt Engineering](./README.md) · [All topics](../README.md)
