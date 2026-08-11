---
title: "What is assertion testing in LLM unit tests?"
id: 173
category: "Evaluation and Testing"
difficulty: "Beginner"
tags:
  - ai-engineering
  - evaluation-and-testing
  - interview-questions
---

# What is assertion testing in LLM unit tests?

**Short answer:** Assertion testing in LLM unit tests applies deterministic rule-based checks (validating valid JSON syntax, regex pattern presence, Pydantic schema validation, output token length, and prohibited word checks) to verify model outputs in software test suites (like PyTest).

## Detail

Relying entirely on expensive LLM-as-a-Judge evaluations for basic format checks is slow and wasteful.

Assertion testing uses fast, deterministic Python assertions as the first line of defense:

```
LLM Generated Output
         │
         ▼
[Deterministic Assertions (PyTest)]
 ├── Assert `json.loads(output)` succeeds (Valid JSON)
 ├── Assert `re.search(r"^\d{5}$", zip_code)` matches
 ├── Assert `"disallowed_word"` NOT in output
 └── Assert `len(tokens)` <= max_tokens
```

### Core Categories of LLM Unit Assertions

1. **Format Assertions:** JSON parsing, valid SQL syntax, Markdown table headers.
2. **Boundary Assertions:** Min/max token length, latency upper bounds ($< 2.0\text{s}$).
3. **Safety Assertions:** Absence of raw PII patterns (SSN, credit card regexes).

## Example

PyTest assertion test suite snippet for LLM outputs:

```python
import json
import pytest

def test_llm_json_output_schema():
    # Simulated LLM output text
    llm_output = '{"user_id": 123, "status": "active"}'
    
    # 1. Assert valid JSON parsing
    try:
        data = json.loads(llm_output)
    except json.JSONDecodeError:
        pytest.fail("LLM output is not valid JSON")
        
    # 2. Assert required keys exist
    assert "user_id" in data, "Missing required key 'user_id'"
    assert "status" in data, "Missing required key 'status'"
    assert isinstance(data["user_id"], int), "'user_id' must be an integer"
```

## Interview tips

- Emphasize combining fast deterministic unit assertions (PyTest) with model-based semantic evals (Ragas / LLM-as-a-Judge).
- Discuss mocking LLM responses in CI unit tests to prevent API token costs during code commits.

## Related Concepts

- [[What is negative prompting and how do you instruct models what not to do?]] (`#112`): [What is negative prompting and how do you instruct models what not to do?](../prompt-engineering/what-is-negative-prompting-and-how-do-you-instruct-models-what-not-to-do.md)
- [[How do you set up automated prompt regression pipelines in GitHub Actions CI/CD?]] (`#166`): [How do you set up automated prompt regression pipelines in GitHub Actions CI/CD?](../llmops-and-production-ai/how-do-you-set-up-automated-prompt-regression-pipelines-in-github-actions-ci-cd.md)
- [[What is exact match (EM) vs F1 score in extraction and classification evals?]] (`#171`): [What is exact match (EM) vs F1 score in extraction and classification evals?](../evaluation-and-testing/what-is-exact-match-em-vs-f1-score-in-extraction-and-classification-evals.md)

---

[⬅ Back to Evaluation and Testing](./README.md) · [All topics](../README.md)
