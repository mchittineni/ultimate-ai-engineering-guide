---
title: "What is PII masking (pseudonymization) and how do Presidio/Regex filters protect user privacy?"
id: 182
category: "AI Safety and Governance"
difficulty: "Beginner"
tags:
  - ai-engineering
  - ai-safety-and-governance
  - interview-questions
---

# What is PII masking (pseudonymization) and how do Presidio/Regex filters protect user privacy?

**Short answer:** PII masking detects Personally Identifiable Information (names, SSNs, credit cards, email addresses, phone numbers) in user text using Named Entity Recognition (NER) models (e.g. Microsoft Presidio) and regex rules, substituting sensitive strings with placeholder tokens before sending prompts to third-party LLM APIs. When the substitution is reversible it is _pseudonymization_, not anonymization.

## Detail

Transmitting raw user PII to cloud LLM vendors risks regulatory violations under GDPR, HIPAA, and CCPA.

### Masking vs Pseudonymization vs Anonymization

These are three different things and the distinction is legal, not stylistic:

| Technique                                                        | Reversible?                               | GDPR status                                         |
| ---------------------------------------------------------------- | ----------------------------------------- | --------------------------------------------------- |
| **Masking / redaction** (`****-****-1234`, or dropping the span) | No, but partial values may still identify | Depends on residual identifiability                 |
| **Pseudonymization** (placeholder + vault, as below)             | Yes, by whoever holds the vault           | **Still personal data** — Art. 4(5), fully in scope |
| **Anonymization** (irreversible, no key retained)                | No                                        | Out of GDPR scope entirely — Recital 26             |

The re-hydration step that makes these pipelines usable is precisely what keeps them in scope: if you can restore `John Doe`, so can anyone who compromises the vault. Art. 32 still credits pseudonymization as a security measure, so this is a control worth having — it just reduces blast radius rather than discharging the obligation. Claiming "we anonymize before sending to the LLM" when a vault exists is a misstatement auditors do catch.

```text
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

### Re-identification Mapping

In interactive applications, a secure local proxy maintains a session mapping dictionary (`<PERSON_1> -> John Doe`) to restore original PII values in model outputs presented to the user. That dictionary is a plaintext concentration of exactly the data you are protecting — keep it session-scoped, encrypted at rest, and expired with the conversation.

## Example

Python PII regex redactor implementation:

```python
import re

def mask_pii_regex(text: str) -> tuple[str, dict]:
    mapping: dict[str, str] = {}
    seen: dict[str, str] = {}

    # 1. Mask Email Addresses -- one stable token per distinct value, so that
    #    a repeated address stays recognisable as the same person to the model.
    def email_repl(m: re.Match) -> str:
        value = m.group(0)
        if value not in seen:
            token = f"<EMAIL_{len(mapping) + 1}>"
            seen[value] = token
            mapping[token] = value
        return seen[value]

    text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', email_repl, text)
    return text, mapping


clean_text, map_dict = mask_pii_regex("Contact Alice at alice@acme.com or alice@acme.com.")
print("Sanitized Text:", clean_text)
# Sanitized Text: Contact Alice at <EMAIL_1> or <EMAIL_1>.
print("Internal Mapping:", map_dict)
# Internal Mapping: {'<EMAIL_1>': 'alice@acme.com'}
```

## Interview tips

- Contrast regex filtering (fast, rule-based for formatted strings like SSN/Credit Card) with NER models (contextual ML for detecting human names and locations).
- Discuss zero data retention (ZDR) business agreements with commercial LLM providers.
- Use the vocabulary precisely: masking, pseudonymization, and anonymization carry different obligations, and only irreversible anonymization exits GDPR scope. Many teams say "anonymization" for all three — correcting that gently is a credibility signal in a regulated-industry interview.
- For the end-to-end redaction/re-hydration pipeline and its failure modes, see [How do you redact PII before sending prompts to LLMs?](./how-do-you-redact-pii-personally-identifiable-information-before-sending-prompts-to-llms.md) (`#44`).

## Related Concepts

- [[What is structured logging for LLM prompts, completions, and token metrics?]] (`#161`): [What is structured logging for LLM prompts, completions, and token metrics?](../llmops-and-production-ai/what-is-structured-logging-for-llm-prompts-completions-and-token-metrics.md)
- [[How to handle confidential enterprise telemetry and PII sanitization in compliance-heavy industries?]] (`#170`): [How to handle confidential enterprise telemetry and PII sanitization in compliance-heavy industries?](../llmops-and-production-ai/how-to-handle-confidential-enterprise-telemetry-and-pii-sanitization-in-compliance-heavy-industries.md)
- [[How to enforce Role-Based Access Control (RBAC) filtering in multi-tenant RAG vector search?]] (`#188`): [How to enforce Role-Based Access Control (RBAC) filtering in multi-tenant RAG vector search?](../ai-safety-and-governance/how-to-enforce-role-based-access-control-rbac-filtering-in-multi-tenant-rag-vector-search.md)

---

[⬅ Back to AI Safety and Governance](./README.md) · [All topics](../README.md)
