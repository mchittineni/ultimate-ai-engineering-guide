---
title: "What is ground-truth reference data in evaluation harnesses?"
id: 88
category: "Evaluation and Testing"
difficulty: "Beginner"
tags:
  - ai-engineering
  - evaluation-and-testing
  - interview-questions
---

# What is ground-truth reference data in evaluation harnesses?

**Short answer:** Ground-truth reference data is a curated, verified dataset of ideal input-output query pairs (and reference context documents) created by domain experts to serve as the baseline benchmark against which candidate LLM prompts, RAG pipelines, and model checkpoints are objectively scored.

## Detail

Without ground-truth reference data, evaluating LLM pipeline quality relies on subjective manual inspection.

```
[Golden Reference Dataset] ──► (Run Candidate Model) ──► Compare Output vs Ground Truth
(50-200 Human-Verified Pairs)                                    │
                                                                 ▼
                                                    [Objective Benchmark Score]
```

### Key Components of a Golden Dataset

1. **Input Queries:** Diverse collection of real-world user prompts, covering core edge cases, multi-turn questions, and adversarial inputs.
2. **Reference Answers:** High-quality, human-verified ideal responses.
3. **Reference Context Snippets:** Ground-truth passages required to answer the question.

### Building & Maintaining Golden Datasets

- **Human-in-the-Loop Curation:** Domain experts annotate baseline answers.
- **Synthetic Data Generation:** Using frontier models (GPT-4o) to generate candidate question-answer pairs from raw documents, followed by human spot-verification.

## Example

JSON structure for an evaluation dataset item:

```json
{
  "id": "eval_042",
  "question": "What is the refund policy for annual enterprise subscriptions?",
  "reference_context": "Annual enterprise subscriptions are eligible for a 100% refund within 14 days of purchase.",
  "reference_answer": "Customers can request a full refund within 14 days of purchasing an annual enterprise subscription.",
  "category": "billing_policy"
}
```

## Interview tips

- Discuss dataset version control: storing golden eval datasets in Git alongside code.
- Highlight the risk of golden dataset stale drift when business policies change.

---

[⬅ Back to Evaluation and Testing](./README.md) · [All topics](../README.md)
