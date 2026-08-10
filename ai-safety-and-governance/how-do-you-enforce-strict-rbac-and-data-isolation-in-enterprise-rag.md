---
title: "How do you enforce strict RBAC and data isolation in enterprise RAG?"
id: 95
category: "AI Safety and Governance"
difficulty: "Advanced"
tags:
  - ai-engineering
  - ai-safety-and-governance
  - interview-questions
---

# How do you enforce strict RBAC and data isolation in enterprise RAG?

**Short answer:** Strict Role-Based Access Control (RBAC) and data isolation in enterprise RAG are enforced by attaching security metadata tags (user groups, tenant IDs) to vector document chunks during ingestion and applying pre-filtering query constraints at the vector database retrieval level before vector similarity search occurs.

## Detail

In multi-tenant enterprise systems, a user in Department A (e.g. Sales) must never retrieve or see confidential context documents belonging to Department B (e.g. Executive HR/Payroll).

```text
[Document Ingest Pipeline] ──► Tag Metadata: {"tenant_id": "org_42", "allowed_roles": ["finance"]}
                                                              │
[User Query from Sales (Role: "sales")]                        ▼
                                                     [Vector DB Search]
                                            Filter: tenant_id == "org_42" AND "sales" IN allowed_roles
                                                              │
                                                              ▼
                                               Zero HR Documents Retrieved
```

### Pre-Filtering vs Post-Filtering

1. **Post-Filtering (Flawed):** Perform vector search top-100, then filter out documents the user lacks permission to view. If top-100 matches are all restricted HR documents, post-filtering returns 0 results to the user even if accessible sales documents existed at rank 101.
2. **Pre-Filtering (Production Standard):** Enforce metadata filtering inside the HNSW vector index graph traversal. Vector search explores only node vectors matching tenant/role constraints.

## Example

Python concept illustrating vector database metadata pre-filtering (Qdrant/Pinecone pattern):

```python
def build_secure_vector_query(user_id: str, user_tenant: str, user_roles: list[str], query_vector: list[float]):
    # Metadata filter applied PRIOR to ANN vector search
    metadata_filter = {
        "must": [
            {"key": "tenant_id", "match": {"value": user_tenant}},
            {"key": "allowed_roles", "match": {"any": user_roles}}
        ]
    }
    # Execute vector search with metadata constraint
    return {"vector": query_vector, "filter": metadata_filter, "top_k": 5}
```

## Interview tips

- Emphasize that pre-filtering guarantees data isolation at the infrastructure level, preventing data leakage regardless of prompt injection attacks.
- Discuss tenant isolation models: shared vector indexes with metadata filtering vs dedicated per-tenant vector indexes.

---

[⬅ Back to AI Safety and Governance](./README.md) · [All topics](../README.md)
