---
title: "How do you set up automated prompt regression pipelines in GitHub Actions CI/CD?"
id: 166
category: "LLMOps and Production AI"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - llmops-and-production-ai
  - interview-questions
---

# How do you set up automated prompt regression pipelines in GitHub Actions CI/CD?

**Short answer:** An automated prompt regression CI/CD pipeline runs a suite of golden evaluation benchmarks against candidate system prompt updates in GitHub Actions pull requests, asserting that accuracy, output schemas, and faithfulness metrics meet required thresholds before code merges to `main`.

## Detail

Modifying system prompt text without regression testing risks breaking production output structures or degrading accuracy on edge-case user queries.

```text
Pull Request Opened (Prompt Update) ──► GitHub Actions CI Trigger
                                                 │
                                                 ▼
                             Run PyTest Eval Harness (50 Golden QA Pairs)
                                                 │
                   ┌─────────────────────────────┴─────────────────────────────┐
                   ▼ (Eval Accuracy >= 95%)                                    ▼ (Eval Accuracy < 95%)
            Pass CI & Allow Merge                                      Block PR & Comment Regression Report
```

### Key Components of Prompt CI/CD

1. **Golden Evaluation Dataset:** Version-controlled JSON file containing ground-truth question-answer pairs.
2. **Automated Evaluator:** PyTest harness calling target model endpoints and scoring output match via LLM-as-a-Judge or exact assertion rules.
3. **PR Comment Bot:** Automatically posting evaluation score comparison tables directly on pull requests.

## Example

GitHub Actions workflow file snippet (`.github/workflows/prompt-eval.yml`):

```yaml
name: Prompt Regression Evaluation

on:
  pull_request:
    paths:
      - 'prompts/**'

jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Run Prompt Eval Harness
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: python3 -m pytest tests/test_prompt_evals.py
```

## Interview tips

- Discuss mocking LLM responses during unit tests vs executing live API calls during integration eval suites.
- Connect prompt CI/CD pipelines to cost control during automated pull request runs.

## Related Concepts

- [[How does Automatic Prompt Engineer (APE) optimize prompt selection using search?]] (`#118`): [How does Automatic Prompt Engineer (APE) optimize prompt selection using search?](../prompt-engineering/how-does-automatic-prompt-engineer-ape-optimize-prompt-selection-using-search.md)
- [[What is semantic versioning for prompts and model configurations in production deployments?]] (`#164`): [What is semantic versioning for prompts and model configurations in production deployments?](../llmops-and-production-ai/what-is-semantic-versioning-for-prompts-and-model-configurations-in-production-deployments.md)
- [[What is assertion testing in LLM unit tests?]] (`#173`): [What is assertion testing in LLM unit tests?](../evaluation-and-testing/what-is-assertion-testing-in-llm-unit-tests.md)

---

[⬅ Back to LLMOps and Production AI](./README.md) · [All topics](../README.md)
