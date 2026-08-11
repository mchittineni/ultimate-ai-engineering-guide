---
title: "AI Safety and Governance"
category: "AI Safety and Governance"
tags:
  - ai-engineering
  - ai-safety-and-governance
  - index
---

# AI Safety and Governance

Data privacy, PII masking, guardrails (NeMo, Llama Guard), alignment tax, copyright, and responsible AI deployment.

**25 questions** · 🟢 Beginner: 11 · 🟡 Intermediate: 8 · 🔴 Advanced: 6

## Questions

| #   | Question                                                                                                                                                                                                         | Difficulty      |
| --- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 10  | [How do input and output guardrails prevent jailbreaks and data leaks?](./how-do-input-and-output-guardrails-prevent-jailbreaks-and-data-leaks.md)                                                               | 🟡 Intermediate |
| 43  | [What is prompt injection and how does it differ from SQL injection?](./what-is-prompt-injection-and-how-does-it-differ-from-sql-injection.md)                                                                   | 🟢 Beginner     |
| 44  | [How do you redact PII (Personally Identifiable Information) before sending prompts to LLMs?](./how-do-you-redact-pii-personally-identifiable-information-before-sending-prompts-to-llms.md)                     | 🟢 Beginner     |
| 45  | [How does Llama Guard classify unsafe inputs and outputs?](./how-does-llama-guard-classify-unsafe-inputs-and-outputs.md)                                                                                         | 🟡 Intermediate |
| 46  | [What is the alignment tax and how does it impact model reasoning?](./what-is-the-alignment-tax-and-how-does-it-impact-model-reasoning.md)                                                                       | 🔴 Advanced     |
| 91  | [What is system prompt exfiltration and how to prevent it?](./what-is-system-prompt-exfiltration-and-how-to-prevent-it.md)                                                                                       | 🟢 Beginner     |
| 92  | [What is data exfiltration via LLM tool calls?](./what-is-data-exfiltration-via-llm-tool-calls.md)                                                                                                               | 🟢 Beginner     |
| 93  | [What is hallucination and what are its primary causes?](./what-is-hallucination-and-what-are-its-primary-causes.md)                                                                                             | 🟢 Beginner     |
| 94  | [How do NeMo Guardrails enforce programmable rails using Colang?](./how-do-nemo-guardrails-enforce-programmable-rails-using-colang.md)                                                                           | 🟡 Intermediate |
| 95  | [How do you enforce strict RBAC and data isolation in enterprise RAG?](./how-do-you-enforce-strict-rbac-and-data-isolation-in-enterprise-rag.md)                                                                 | 🔴 Advanced     |
| 181 | [What is indirect prompt injection and how does it occur when parsing web pages/documents?](./what-is-indirect-prompt-injection-and-how-does-it-occur-when-parsing-web-pages-documents.md)                       | 🟢 Beginner     |
| 182 | [What is PII masking (pseudonymization) and how do Presidio/Regex filters protect user privacy?](./what-is-pii-masking-pseudonymization-and-how-do-presidio-regex-filters-protect-user-privacy.md)               | 🟢 Beginner     |
| 183 | [What is copyright infringement risk in RAG and fine-tuning datasets?](./what-is-copyright-infringement-risk-in-rag-and-fine-tuning-datasets.md)                                                                 | 🟢 Beginner     |
| 184 | [What is model jailbreaking and how do safety classifiers block it?](./what-is-model-jailbreaking-and-how-do-safety-classifiers-block-it.md)                                                                     | 🟢 Beginner     |
| 185 | [What is data lineage tracking for RAG documents and enterprise vector stores?](./what-is-data-lineage-tracking-for-rag-documents-and-enterprise-vector-stores.md)                                               | 🟢 Beginner     |
| 186 | [How to prevent Data Exfiltration via Markdown image tags and hidden web beacons in LLM outputs?](./how-to-prevent-data-exfiltration-via-markdown-image-tags-and-hidden-web-beacons-in-llm-outputs.md)           | 🟡 Intermediate |
| 187 | [How does Llama Guard taxonomy classify unsafe inputs and outputs across safety categories?](./how-does-llama-guard-taxonomy-classify-unsafe-inputs-and-outputs-across-safety-categories.md)                     | 🟡 Intermediate |
| 188 | [How to enforce Role-Based Access Control (RBAC) filtering in multi-tenant RAG vector search?](./how-to-enforce-role-based-access-control-rbac-filtering-in-multi-tenant-rag-vector-search.md)                   | 🟡 Intermediate |
| 189 | [How do NeMo Guardrails use Colang state flows to strictly control conversation trajectories?](./how-do-nemo-guardrails-use-colang-state-flows-to-strictly-control-conversation-trajectories.md)                 | 🔴 Advanced     |
| 190 | [How to audit and secure Model Context Protocol (MCP) servers against unauthorized tool invocation?](./how-to-audit-and-secure-model-context-protocol-mcp-servers-against-unauthorized-tool-invocation.md)       | 🔴 Advanced     |
| 201 | [What is model inversion and membership inference, and how do you defend against them?](./what-is-model-inversion-and-membership-inference-and-how-do-you-defend-against-them.md)                                | 🔴 Advanced     |
| 202 | [What is training data poisoning and how do backdoor triggers survive fine-tuning?](./what-is-training-data-poisoning-and-how-do-backdoor-triggers-survive-fine-tuning.md)                                       | 🔴 Advanced     |
| 203 | [What is model supply chain security and why are serialized model weights dangerous?](./what-is-model-supply-chain-security-and-why-are-serialized-model-weights-dangerous.md)                                   | 🟡 Intermediate |
| 204 | [How does the EU AI Act classify AI systems into risk tiers?](./how-does-the-eu-ai-act-classify-ai-systems-into-risk-tiers.md)                                                                                   | 🟡 Intermediate |
| 205 | [What is the NIST AI Risk Management Framework and how do its four functions structure AI governance?](./what-is-the-nist-ai-risk-management-framework-and-how-do-its-four-functions-structure-ai-governance.md) | 🟢 Beginner     |

## What interviewers probe here

- Implementing input/output guardrails using Llama Guard or NeMo.
- Redacting PII and enforcing data isolation in multi-tenant RAG systems.
- Managing the alignment tax: balancing safety interventions with model capability.

---

[⬅ Back to all topics](../README.md)
