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

**Short answer:** Redacting Personally Identifiable Information (PII) uses local Named Entity Recognition (NER) models (e.g. Microsoft Presidio, SpaCy) and regex pattern engines to intercept text before API transmission, replacing sensitive tokens (names, SSNs, credit card numbers, email addresses) with reversible placeholders, and re-hydrating those placeholders upon receiving the LLM response. Because the mapping is reversible this is pseudonymization under GDPR Art. 4(5), not anonymization — the data stays in regulatory scope.

## Detail

Sending un-redacted PII to an external cloud LLM provider is a regulated data transfer, not automatically a violation: under GDPR it needs a lawful basis plus a Data Processing Agreement, and under HIPAA it needs a Business Associate Agreement with the provider. Redaction is the control you apply when you cannot rely on those agreements, when the provider is outside your compliance boundary, or when you want to shrink blast radius on principle. (SOC 2 is an audit framework rather than a privacy law, but auditors will ask how egress is controlled.)

> **Say "pseudonymization," not "anonymization."** Because the pipeline below keeps a vault that maps `<NAME_1>` back to `John Doe`, the transformation is reversible, which under GDPR Art. 4(5) makes it **pseudonymization** — and pseudonymized data is still personal data, fully in scope for the regulation. Anonymization means irreversible, no-key-anywhere de-identification, which by construction cannot support the re-hydration step users expect. Calling a reversible vault "anonymization" in an interview (or a DPIA) is a substantive error: it implies the GDPR obligations have been discharged when they have not. Pseudonymization is still worth doing — Art. 32 names it as a security measure — it just shrinks blast radius rather than exiting scope.

### The Redaction-Rehydration Pipeline

```text
[User Input with PII] ──► [Local PII Engine (Presidio)] ──► Replace with Placeholders
                                                                    │
                                                                    ▼
[User Output] ◄── [Re-hydration Vault] ◄── [LLM Provider] ◄── [Anonymized Prompt]
```

1. **Detection:** Run NER models and pattern matchers locally (e.g., regex for credit cards/SSNs, Transformer NER for patient names).
2. **Pseudonymization:** Replace PII tokens with mapped placeholders (e.g., `John Doe` $\rightarrow$ `<NAME_1>`, `john@example.com` $\rightarrow$ `<EMAIL_1>`).
3. **Transmission:** Send the pseudonymized prompt to the third-party LLM API.
4. **Re-hydration:** Intercept the LLM completion and swap placeholders back to original values before rendering to authorized end users.

The vault is the sensitive asset in this design — it is a plaintext index of exactly the data you were trying to protect. Scope it to the session, keep it in memory or an encrypted store, and expire it with the conversation.

## Example

Python concept using Microsoft Presidio or custom regex mapper:

```python
import re

PII_PATTERNS = {
    "EMAIL": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "PHONE": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"
}

def pseudonymize_text(text: str) -> tuple[str, dict]:
    """Replace PII with placeholders, returning the text and the re-hydration vault.

    Two details the naive version gets wrong:

    1. It iterates `re.findall` results and calls `str.replace(match, ...)`, which
       rewrites *every* occurrence on the first pass. A value appearing twice
       therefore mints a second placeholder that matches nothing in the text --
       a vault entry that can never be re-hydrated, and a silent drift between
       what was sent and what you can restore.
    2. Assigning one placeholder per *occurrence* rather than per *distinct
       value* also destroys coreference: the model can no longer tell that
       `<EMAIL_1>` and `<EMAIL_2>` are the same person.

    Substituting via `re.sub` with a callback fixes both -- each distinct value
    gets exactly one stable placeholder, and every occurrence maps back to it.
    """
    vault: dict[str, str] = {}
    seen: dict[tuple[str, str], str] = {}

    def substitute(pii_type: str):
        def repl(match: re.Match) -> str:
            value = match.group(0)
            key = (pii_type, value)
            if key not in seen:
                placeholder = f"<{pii_type}_{sum(1 for k in seen if k[0] == pii_type) + 1}>"
                seen[key] = placeholder
                vault[placeholder] = value
            return seen[key]

        return repl

    pseudonymized = text
    for pii_type, pattern in PII_PATTERNS.items():
        pseudonymized = re.sub(pattern, substitute(pii_type), pseudonymized)
    return pseudonymized, vault


def rehydrate(text: str, vault: dict) -> str:
    for placeholder, value in vault.items():
        text = text.replace(placeholder, value)
    return text


raw_text = "Email jane.doe@example.com, cc jane.doe@example.com, or call 555-123-4567."
clean, vault = pseudonymize_text(raw_text)
print("Pseudonymized:", clean)
# Pseudonymized: Email <EMAIL_1>, cc <EMAIL_1>, or call <PHONE_1>.
print("Vault mapping:", vault)
# Vault mapping: {'<EMAIL_1>': 'jane.doe@example.com', '<PHONE_1>': '555-123-4567'}
assert rehydrate(clean, vault) == raw_text  # round-trips exactly
```

## Interview tips

- Emphasize that PII detection must occur locally on enterprise infrastructure before network egress to external LLM providers.
- Mention edge cases in medical (HIPAA) and financial contexts where context-aware NER models out-perform simple regex matching.
- Use the precise term. Reversible vault mapping is pseudonymization; irreversible de-identification is anonymization. Interviewers in regulated industries listen for this, because only the second one takes data out of GDPR scope.
- Be honest about detection recall: NER misses PII, and a miss is a silent egress of real user data. Quote a measured recall number on your own corpus and describe the fallback (block on low-confidence spans, or route the request to a self-hosted model) rather than claiming the filter is complete.

---

[⬅ Back to AI Safety and Governance](./README.md) · [All topics](../README.md)
