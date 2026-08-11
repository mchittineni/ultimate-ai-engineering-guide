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

```text
Kappa Score Interpretation (Landis & Koch):
  0.00 - 0.20 ──► Slight Agreement      (Do NOT trust this LLM judge)
  0.21 - 0.40 ──► Fair Agreement
  0.41 - 0.60 ──► Moderate Agreement
  0.61 - 0.80 ──► Substantial Agreement (usable with spot-checking)
  0.81 - 1.00 ──► Almost Perfect Agreement
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
# 0.583 -> Moderate agreement. Note that 8/10 raw agreement sounds strong but
# collapses to kappa 0.58 once chance agreement (P_e = 0.52) is removed -- which
# is exactly why raw accuracy is the wrong way to validate a judge.
```

## Interview tips

- Highlight that a low Kappa score indicates ambiguous evaluation rubrics or judge prompt bias (position or verbosity bias).
- Discuss refining judge rubrics to increase Kappa agreement scores above 0.70.

---

[⬅ Back to Evaluation and Testing](./README.md) · [All topics](../README.md)
