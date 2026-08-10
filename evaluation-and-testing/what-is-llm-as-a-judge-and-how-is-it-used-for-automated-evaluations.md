---
title: "What is LLM-as-a-Judge and how is it used for automated evaluations?"
id: 39
category: "Evaluation and Testing"
difficulty: "Beginner"
tags:
  - ai-engineering
  - evaluation-and-testing
  - interview-questions
---

# What is LLM-as-a-Judge and how is it used for automated evaluations?

**Short answer:** LLM-as-a-Judge uses a powerful LLM (e.g. GPT-4o or Claude 3.5 Sonnet) with structured rubrics to automatically grade, score, or compare candidate model outputs for qualitative criteria like accuracy, helpfulness, tone, safety, and format adherence.

## Detail

Traditional NLP metrics like BLEU or ROUGE perform exact n-gram matching, failing to assess semantic correctness or reasoning quality. Human evaluation is slow and unscalable. LLM-as-a-Judge bridges this gap.

### Common Judge Setup Configurations

1. **Single-Answer Scoring:** The judge rates a generated answer on a Likert scale (1-5 or 1-10) against an explicit grading rubric.
2. **Pairwise Comparison (A/B Testing):** The judge receives two outputs (Model A vs Model B) for a given prompt and selects the winning response (or tie).
3. **Reference-Based Evaluation:** The judge compares the generated response against a human-written ground truth reference answer.

```text
[Prompt + Candidate Output + Scoring Rubric] ──► [Judge LLM] ──► Structured Grade + Rationale
```

## Example

Python prompt template for a single-answer judge evaluation:

```python
judge_prompt_template = """You are an expert evaluator scoring an AI assistant response.

[User Question]
{question}

[AI Response]
{response}

[Scoring Rubric]
Score 1: Completely inaccurate or unhelpful.
Score 3: Partially correct but missing key detail.
Score 5: Exceptionally clear, fully accurate, and directly answers the question.

Provide your evaluation in valid JSON with fields "explanation" and "score" (integer 1-5)."""
```

## Interview tips

- Highlight position bias (in pairwise comparison, judges often favor whichever response appears first as Candidate A) and verbosity bias (judges favor longer outputs).
- Explain swap evaluation: running pairwise comparisons twice with candidate order swapped to eliminate position bias.

---

[⬅ Back to Evaluation and Testing](./README.md) · [All topics](../README.md)
