---
title: "How to enforce Role-Based Access Control (RBAC) filtering in multi-tenant RAG vector search?"
id: 188
category: "AI Safety and Governance"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - ai-safety-and-governance
  - interview-questions
---

# How to enforce Role-Based Access Control (RBAC) filtering in multi-tenant RAG vector search?

**Short answer:** Enforcing RBAC filtering in multi-tenant RAG attaches user role and tenant metadata (`allowed_roles: ["engineering", "legal"]`, `tenant_id: "acme"`) to vector chunks during ingestion, applying pre-filtering query constraints at the vector database retrieval layer to guarantee that users retrieve only context documents matching their active security permissions.

## Detail

In enterprise multi-tenant systems, unauthorized context retrieval causes severe data leaks (e.g. an engineer accidentally retrieving confidential executive salary documents).

```
User Token: {user_id: "u123", tenant_id: "corp_42", roles: ["engineering"]}
                                    │
                                    ▼
[Vector Database Pre-Filter]
Must Match: `tenant_id == "corp_42"` AND `allowed_roles CONTAINS "engineering"`
                                    │
                                    ▼
            ANN Vector Search Executed ONLY on Authorized Nodes
```

### Key Security Guarantee

- **Pre-Filtering vs Prompt Instructions:** System prompt instructions (*"Do not reveal executive salary info"*) are soft constraints that prompt injection attacks can bypass. Metadata pre-filtering enforces strict access control at the infrastructure database level.

## Example

Python Qdrant/Pinecone RBAC pre-filter constructor:

```python
def build_rbac_vector_filter(user_tenant_id: str, user_roles: list[str]) -> dict:
    return {
        "must": [
            {"key": "tenant_id", "match": {"value": user_tenant_id}},
            {"key": "allowed_roles", "match": {"any": user_roles}}
        ]
    }

rbac_filter = build_rbac_vector_filter("org_acme", ["sales_rep", "regional_manager"])
print("RBAC Vector Pre-Filter Payload:\n", rbac_filter)
```

## Interview tips

- Highlight that pre-filtering inside vector index graph traversal prevents data leaks regardless of prompt injection attacks.
- Discuss tenant isolation options: single shared vector collection with metadata pre-filtering vs dedicated per-tenant vector collections.

## Related Concepts

- [[What is document metadata filtering in vector databases?]] (`#123`): [What is document metadata filtering in vector databases?](../rag-and-vector-databases/what-is-document-metadata-filtering-in-vector-databases.md)
- [[How to handle confidential enterprise telemetry and PII sanitization in compliance-heavy industries?]] (`#170`): [How to handle confidential enterprise telemetry and PII sanitization in compliance-heavy industries?](../llmops-and-production-ai/how-to-handle-confidential-enterprise-telemetry-and-pii-sanitization-in-compliance-heavy-industries.md)
- [[What is data lineage tracking for RAG documents and enterprise vector stores?]] (`#185`): [What is data lineage tracking for RAG documents and enterprise vector stores?](../ai-safety-and-governance/what-is-data-lineage-tracking-for-rag-documents-and-enterprise-vector-stores.md)

---

[⬅ Back to AI Safety and Governance](./README.md) · [All topics](../README.md)
