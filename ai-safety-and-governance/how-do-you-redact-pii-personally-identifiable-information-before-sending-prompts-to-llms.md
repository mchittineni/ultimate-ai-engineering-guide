---
title: "How do you redact PII (Personally Identifiable Information) before sending prompts to LLMs?"
id: 44
category: "AI Safety and Governance"
difficulty: "Beginner"
tags:
  - ai-engineering
  - ai-safety-and-governance
  - interview-questions
---

# How do you redact PII (Personally Identifiable Information) before sending prompts to LLMs?

**Short answer:** Redacting Personally Identifiable Information (PII) uses local Named Entity Recognition (NER) models (e.g. Microsoft Presidio, SpaCy) and regex pattern engines to intercept text before API transmission, replacing sensitive tokens (names, SSNs, credit card numbers, email addresses) with anonymized placeholders, and re-hydrating placeholders upon receiving the LLM response.

## Detail

Sending un-redacted PII to an external cloud LLM provider is a regulated data transfer, not automatically a violation: under GDPR it needs a lawful basis plus a Data Processing Agreement, and under HIPAA it needs a Business Associate Agreement with the provider. Redaction is the control you apply when you cannot rely on those agreements, when the provider is outside your compliance boundary, or when you want to shrink blast radius on principle. (SOC 2 is an audit framework rather than a privacy law, but auditors will ask how egress is controlled.)

### The Redaction-Rehydration Pipeline

```text
[User Input with PII] ──► [Local PII Engine (Presidio)] ──► Replace with Placeholders
                                                                    │
                                                                    ▼
[User Output] ◄── [Re-hydration Vault] ◄── [LLM Provider] ◄── [Anonymized Prompt]
```

1. **Detection:** Run NER models and pattern matchers locally (e.g., regex for credit cards/SSNs, Transformer NER for patient names).
2. **Anonymization:** Replace PII tokens with mapped placeholders (e.g., `John Doe` $\rightarrow$ `<NAME_1>`, `john@example.com` $\rightarrow$ `<EMAIL_1>`).
3. **Transmission:** Send anonymized prompt to third-party LLM API.
4. **Re-hydration:** Intercept the LLM completion and swap placeholders back to original values before rendering to authorized end users.

## Example

Python concept using Microsoft Presidio or custom regex mapper:

```python
import re

PII_PATTERNS = {
    "EMAIL": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "PHONE": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"
}

def anonymize_text(text: str) -> tuple[str, dict]:
    vault = {}
    anonymized = text
    for pii_type, pattern in PII_PATTERNS.items():
        matches = re.findall(pattern, anonymized)
        for idx, match in enumerate(matches):
            placeholder = f"<{pii_type}_{idx+1}>"
            vault[placeholder] = match
            anonymized = anonymized.replace(match, placeholder)
    return anonymized, vault

raw_text = "Contact Jane at jane.doe@example.com or call 555-123-4567."
anon, vault = anonymize_text(raw_text)
print("Anonymized:", anon)
print("Vault mapping:", vault)
```

## Interview tips

- Emphasize that PII detection must occur locally on enterprise infrastructure before network egress to external LLM providers.
- Mention edge cases in medical (HIPAA) and financial contexts where context-aware NER models out-perform simple regex matching.

---

[⬅ Back to AI Safety and Governance](./README.md) · [All topics](../README.md)
