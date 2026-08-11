---
title: "What is PII masking (anonymization) and how do Presidio/Regex filters protect user privacy?"
id: 182
category: "AI Safety and Governance"
difficulty: "Beginner"
tags:
  - ai-engineering
  - ai-safety-and-governance
  - interview-questions
---

# What is PII masking (anonymization) and how do Presidio/Regex filters protect user privacy?

**Short answer:** PII masking (anonymization) detects Personally Identifiable Information (names, SSNs, credit cards, email addresses, phone numbers) in user text using Named Entity Recognition (NER) models (e.g. Microsoft Presidio) and regex rules, substituting sensitive strings with anonymized tokens before sending prompts to third-party LLM APIs.

## Detail

Transmitting raw user PII to cloud LLM vendors risks regulatory violations under GDPR, HIPAA, and CCPA.

```
Raw User Input:  "My name is John Doe, SSN 123-45-6789. Can you check my account?"
                                       │
                                       ▼
                  [Microsoft Presidio PII Engine]
                                       │
                                       ▼
Sanitized Input: "My name is <PERSON_1>, SSN <US_SSN_1>. Can you check my account?"
                                       │
                                       ▼
                  [Send to Third-Party LLM API]
```

### De-anonymization Mapping

In interactive applications, a secure local proxy maintains a session mapping dictionary (`<PERSON_1> -> John Doe`) to restore original PII values in model outputs presented to the user.

## Example

Python PII regex redactor implementation:

```python
import re

def mask_pii_regex(text: str) -> tuple[str, dict]:
    mapping = {}
    
    # 1. Mask Email Addresses
    def email_repl(m):
        token = f"<EMAIL_{len(mapping)}>"
        mapping[token] = m.group(0)
        return token
        
    text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', email_repl, text)
    return text, mapping

clean_text, map_dict = mask_pii_regex("Contact Alice at alice@acme.com for support.")
print("Sanitized Text:", clean_text)
print("Internal Mapping:", map_dict)
```

## Interview tips

- Contrast regex filtering (fast, rule-based for formatted strings like SSN/Credit Card) with NER models (contextual ML for detecting human names and locations).
- Discuss zero data retention (ZDR) business agreements with commercial LLM providers.

## Related Concepts

- [[What is structured logging for LLM prompts, completions, and token metrics?]] (`#161`): [What is structured logging for LLM prompts, completions, and token metrics?](../llmops-and-production-ai/what-is-structured-logging-for-llm-prompts-completions-and-token-metrics.md)
- [[How to handle confidential enterprise telemetry and PII sanitization in compliance-heavy industries?]] (`#170`): [How to handle confidential enterprise telemetry and PII sanitization in compliance-heavy industries?](../llmops-and-production-ai/how-to-handle-confidential-enterprise-telemetry-and-pii-sanitization-in-compliance-heavy-industries.md)
- [[How to enforce Role-Based Access Control (RBAC) filtering in multi-tenant RAG vector search?]] (`#188`): [How to enforce Role-Based Access Control (RBAC) filtering in multi-tenant RAG vector search?](../ai-safety-and-governance/how-to-enforce-role-based-access-control-rbac-filtering-in-multi-tenant-rag-vector-search.md)

---

[⬅ Back to AI Safety and Governance](./README.md) · [All topics](../README.md)
