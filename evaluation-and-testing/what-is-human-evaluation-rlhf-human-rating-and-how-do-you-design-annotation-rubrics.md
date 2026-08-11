---
title: "What is human evaluation (RLHF human rating) and how do you design annotation rubrics?"
id: 175
category: "Evaluation and Testing"
difficulty: "Beginner"
tags:
  - ai-engineering
  - evaluation-and-testing
  - interview-questions
---

# What is human evaluation (RLHF human rating) and how do you design annotation rubrics?

**Short answer:** Human evaluation collects structured feedback from human domain experts who rate model outputs against explicit qualitative criteria; designing resilient annotation rubrics requires establishing unambiguous scoring scales ($1-5$ Likert scales or pairwise comparisons) with explicit positive/negative example guidelines to maximize inter-annotator agreement.

## Detail

While automated metrics are fast, human evaluation remains the gold standard ground-truth for subjective quality, safety, and domain correctness.

```text
Model Generation Output ──► [Human Domain Expert Annotator] ──► Inspects Detailed Rubric
                                                                         │
                                                                         ▼
                                                     Assigns Likert Ratings (1-5)
                                                     - Correctness: 5/5
                                                     - Conciseness: 4/5
                                                     - Harm/Safety: 0/5
```

### Key Principles of Resilient Rubrics

1. **Unambiguous Criteria:** Defining precise score distinctions (e.g. _"Score 3 = Answer is factually correct but includes minor formatting flaws; Score 1 = Factually incorrect"_).
2. **Pairwise vs Absolute Scoring:** Pairwise comparison ("Model A vs Model B") yields higher inter-annotator agreement than absolute 1-10 numerical scoring.
3. **Control Calibration Examples:** Providing annotators with pre-labeled benchmark examples to calibrate scoring tendencies.

## Example

Structured Markdown Human Annotation Rubric Template:

```markdown
### Pairwise Preference Rubric: Customer Support Bot

Given User Query and Candidate Outputs A and B:

1. **Factuality (Pass/Fail):** Does the response contain any ungrounded claims?
2. **Preference Pick:** Choose Winning Response (Model A / Model B / Tie).
   - *Criteria for Win:* Direct answer to query, professional tone, zero hallucination.
```

## Interview tips

- Discuss calculating inter-annotator agreement (Fleiss' Kappa or Cohen's Kappa) to validate annotator consistency.
- Explain using human evaluation data to train reward models for RLHF or DPO alignment.

## Related Concepts

- [[How does Active Prompting dynamically select the best exemplars for few-shot learning?]] (`#117`): [How does Active Prompting dynamically select the best exemplars for few-shot learning?](../prompt-engineering/how-does-active-prompting-dynamically-select-the-best-exemplars-for-few-shot-learning.md)
- [[How does ORPO perform SFT and alignment in a single step without reference models?]] (`#149`): [How does ORPO perform SFT and alignment in a single step without reference models?](../fine-tuning-and-adaptation/how-does-orpo-perform-sft-and-alignment-in-a-single-step-without-reference-models.md)
- [[How to implement Elo rating systems to benchmark model performance?]] (`#179`): [How to implement Elo rating systems to benchmark model performance?](../evaluation-and-testing/how-to-implement-elo-rating-systems-to-benchmark-model-performance.md)

---

[⬅ Back to Evaluation and Testing](./README.md) · [All topics](../README.md)
