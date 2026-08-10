---
title: "How do you measure inter-annotator agreement (Cohen's Kappa) with LLM judges?"
id: 89
category: "Evaluation and Testing"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - evaluation-and-testing
  - interview-questions
---

# How do you measure inter-annotator agreement (Cohen's Kappa) with LLM judges?

**Short answer:** Inter-annotator agreement between LLM judges and human evaluators is measured using statistical metrics like Cohen's Kappa ($\kappa$), which calculates the proportion of agreement beyond chance to validate that an automated LLM judge reliably mirrors human judgment.

## Detail

Before trusting an LLM-as-a-Judge to automate production evaluation pipelines, developers must validate that the judge model agrees with human domain experts.

### Cohen's Kappa Formula

$$\kappa = \frac{P_o - P_e}{1 - P_e}$$

Where:
- $P_o$ is the observed proportional agreement between human annotator and LLM judge.
- $P_e$ is the expected agreement by chance.

```
Kappa Score Interpretation:
  < 0.20  ──► Poor Agreement (Do NOT trust LLM judge)
  0.41 - 0.60 ──► Moderate Agreement
  0.61 - 0.80 ──► Substantial Agreement
  0.81 - 1.00 ──► Near Perfect Alignment (Production-ready LLM judge)
```

## Example

Python calculation of Cohen's Kappa using `scikit-learn`:

```python
from sklearn.metrics import cohen_kappa_score

# Sample ratings (1 = Pass, 0 = Fail) on 10 eval items
human_ratings = [1, 1, 0, 1, 0, 0, 1, 1, 0, 1]
llm_judge_ratings = [1, 1, 0, 1, 1, 0, 1, 1, 0, 0] # Disagrees on 2 items

kappa = cohen_kappa_score(human_ratings, llm_judge_ratings)
print(f"Inter-Annotator Cohen's Kappa: {kappa:.3f}")
# Kappa ~ 0.60 indicates moderate-to-substantial alignment
```

## Interview tips

- Highlight that a low Kappa score indicates ambiguous evaluation rubrics or judge prompt bias (position or verbosity bias).
- Discuss refining judge rubrics to increase Kappa agreement scores above 0.70.

---

[⬅ Back to Evaluation and Testing](./README.md) · [All topics](../README.md)
