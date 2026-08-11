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

Filter syntax is vendor-specific — these are not interchangeable, and writing Qdrant's shape against a Pinecone index is a common review comment:

```python
# Qdrant: `must` clauses over payload keys.
def build_qdrant_filter(user_tenant: str, user_roles: list[str]) -> dict:
    return {
        "must": [
            {"key": "tenant_id", "match": {"value": user_tenant}},
            {"key": "allowed_roles", "match": {"any": user_roles}},
        ]
    }


# Pinecone: MongoDB-style operators.
def build_pinecone_filter(user_tenant: str, user_roles: list[str]) -> dict:
    return {
        "tenant_id": {"$eq": user_tenant},
        "allowed_roles": {"$in": user_roles},
    }


def build_secure_vector_query(user_tenant: str, user_roles: list[str], query_vector: list[float]) -> dict:
    # The filter is applied PRIOR to (and during) ANN traversal, not after.
    return {"vector": query_vector, "filter": build_qdrant_filter(user_tenant, user_roles), "top_k": 5}
```

The security-critical property is not the syntax but where the tenant and role values come from: derive them **server-side from the verified session token**, never from anything the model produced or the client sent. A filter built from LLM output is not an access control — it is the model deciding its own permissions.

## Interview tips

- Emphasize that pre-filtering enforces data isolation at the infrastructure level, so a successful prompt injection still cannot retrieve documents the user's own filter excludes.
- Discuss tenant isolation models: shared vector indexes with metadata filtering vs dedicated per-tenant vector indexes.
- Name the recall cost. Filtering restricts HNSW traversal to matching nodes, so a highly selective filter fragments the graph and degrades recall — which is why Qdrant switches to exact search below a cardinality threshold. Pre-filtering is correct for security and does have a measurable retrieval-quality cost you should benchmark, not assume away.
- Know the syntax of the store you claim to have used. Qdrant `must`/`match`, Pinecone `$eq`/`$in`, Weaviate `where` with `operator`/`valueText`.

---

[⬅ Back to AI Safety and Governance](./README.md) · [All topics](../README.md)
