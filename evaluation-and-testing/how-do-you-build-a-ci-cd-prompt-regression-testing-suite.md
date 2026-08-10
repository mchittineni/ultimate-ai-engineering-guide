---
title: "How do you build a CI/CD prompt regression testing suite?"
id: 41
category: "Evaluation and Testing"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - evaluation-and-testing
  - interview-questions
---

# How do you build a CI/CD prompt regression testing suite?

**Short answer:** A CI/CD prompt regression suite automatically executes a golden evaluation dataset through target prompts or RAG pipelines whenever code or system prompts are changed in Git, scoring outputs using deterministic checks (regex, schema validators) and LLM judges, and blocking pull requests that introduce quality regressions.

## Detail

In traditional software, modifying code triggers unit tests. In LLM engineering, modifying a system prompt or updating an embedding model can silently degrade model accuracy across edge cases.

### CI/CD Pipeline Architecture

```
[PR Opened / Prompt Updated] ──► [GitHub Actions Worker]
                                         │
                   ┌─────────────────────┴─────────────────────┐
                   ▼                                           ▼
       (Run Golden Eval Dataset)                     (Evaluate Responses)
       100 curated domain pairs                       - Schema Validation
                                                      - Ragas / Judge Scoring
                                                               │
                                                               ▼
                                                  [Compare Scores vs Main]
                                                  If Score < Threshold -> Block PR
```

### Key Components

1. **Golden Dataset:** A version-controlled set of 50–200 representative query-answer pairs covering core features and historical edge cases.
2. **Assertion Layer:** Fast deterministic checks (JSON schema validation, prohibited word lists) combined with LLM-as-a-Judge metric scoring.
3. **Threshold Gating:** Failing the build if aggregate faithfulness or accuracy score drops below a baseline threshold (e.g. $> 2\%$ regression).

## Example

Example GitHub Actions workflow snippet executing a prompt evaluation suite (using `promptfoo` or custom pytest script):

```yaml
name: Prompt CI Evaluation

on:
  pull_request:
    paths:
      - 'prompts/**'
      - 'rag/**'

jobs:
  evaluate-prompts:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install pytest pydantic openai
      - name: Run Golden Eval Suite
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: python -m pytest tests/eval_suite.py --threshold=0.90
```

## Interview tips

- Discuss managing LLM API costs in CI: caching eval responses for unchanged prompts and running evaluations on lightweight models (GPT-4o-mini / Llama 3 8B).
- Highlight tracking metric drift over time in dashboards (e.g. LangSmith, Phoenix).

---

[⬅ Back to Evaluation and Testing](./README.md) · [All topics](../README.md)
