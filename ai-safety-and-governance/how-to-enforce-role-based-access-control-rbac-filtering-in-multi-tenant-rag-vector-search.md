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

```text
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

- **Pre-Filtering vs Prompt Instructions:** System prompt instructions (_"Do not reveal executive salary info"_) are soft constraints that prompt injection attacks can bypass. Metadata pre-filtering enforces strict access control at the infrastructure database level.

### Where This Actually Breaks: Permission Freshness

Pre-filtering is sound. The failures in production are almost always about _when_ the permission data was written, not whether the filter ran:

1. **Stale chunk ACLs.** `allowed_roles` is copied onto the chunk at ingestion time. Revoke someone's access in the source system — Sharepoint, Drive, the HRIS — and the vector store keeps serving them until re-indexing. Either re-sync ACLs on a schedule tight enough to satisfy your policy, or store a document ID and resolve permissions live at query time.
2. **Role claims from a stale token.** A long-lived JWT carries the roles held at issuance. Pair short token lifetimes with server-side resolution of the current role set.
3. **Deleted documents that outlive their deletion.** Most vector stores tombstone rather than erase, so a purged document can remain retrievable until compaction.
4. **Filters derived from model output.** If the tenant or role values are parsed from anything the LLM generated, injection controls the filter and the whole scheme collapses. Build filters from the verified session server-side, always.

## Example

RBAC pre-filter constructors — note that the filter syntax differs per vendor:

```python
def build_rbac_vector_filter_qdrant(user_tenant_id: str, user_roles: list[str]) -> dict:
    return {
        "must": [
            {"key": "tenant_id", "match": {"value": user_tenant_id}},
            {"key": "allowed_roles", "match": {"any": user_roles}},
        ]
    }


def build_rbac_vector_filter_pinecone(user_tenant_id: str, user_roles: list[str]) -> dict:
    # Pinecone uses MongoDB-style operators, not Qdrant's must/match shape.
    return {"tenant_id": {"$eq": user_tenant_id}, "allowed_roles": {"$in": user_roles}}


# Values come from the verified session, never from user or model input.
session = {"tenant_id": "org_acme", "roles": ["sales_rep", "regional_manager"]}
print(build_rbac_vector_filter_qdrant(session["tenant_id"], session["roles"]))
print(build_rbac_vector_filter_pinecone(session["tenant_id"], session["roles"]))
```

## Interview tips

- Highlight that pre-filtering inside vector index graph traversal prevents data leaks regardless of prompt injection attacks.
- Discuss tenant isolation options: single shared vector collection with metadata pre-filtering vs dedicated per-tenant vector collections.
- Bring up permission freshness unprompted. Everyone describes the filter; the senior answer is that the filter is only as current as the ACLs denormalized into the index, and names the re-sync or live-resolution strategy.
- For the pre- vs post-filtering recall argument and the HNSW traversal detail, see [How do you enforce strict RBAC and data isolation in enterprise RAG?](./how-do-you-enforce-strict-rbac-and-data-isolation-in-enterprise-rag.md) (`#95`).

## Related Concepts

- [[What is document metadata filtering in vector databases?]] (`#123`): [What is document metadata filtering in vector databases?](../rag-and-vector-databases/what-is-document-metadata-filtering-in-vector-databases.md)
- [[How to handle confidential enterprise telemetry and PII sanitization in compliance-heavy industries?]] (`#170`): [How to handle confidential enterprise telemetry and PII sanitization in compliance-heavy industries?](../llmops-and-production-ai/how-to-handle-confidential-enterprise-telemetry-and-pii-sanitization-in-compliance-heavy-industries.md)
- [[What is data lineage tracking for RAG documents and enterprise vector stores?]] (`#185`): [What is data lineage tracking for RAG documents and enterprise vector stores?](../ai-safety-and-governance/what-is-data-lineage-tracking-for-rag-documents-and-enterprise-vector-stores.md)

---

[⬅ Back to AI Safety and Governance](./README.md) · [All topics](../README.md)
