---
title: "How does semantic caching reduce LLM API latency and cost?"
id: 32
category: "AI System Design"
difficulty: "Beginner"
tags:
  - ai-engineering
  - ai-system-design
  - interview-questions
---

# How does semantic caching reduce LLM API latency and cost?

**Short answer:** Semantic caching stores previously generated LLM responses alongside query vector embeddings in a fast cache (e.g. Redis vector search); incoming queries are embedded and matched against cached queries using cosine similarity—if similarity exceeds a threshold (e.g. 0.92), the cached answer is returned in under 10ms without calling the LLM.

## Detail

Traditional exact-string HTTP caching (e.g. Redis key-value) fails for LLM applications because users phrase the same query in multiple ways (e.g. *"How do I reset my password?"* vs *"Steps to reset password"*).

### Semantic Cache Architecture

```
[User Query] ──► [Embedder] ──► Vector Similarity Search (Redis / Milvus)
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 ▼ (Similarity >= 0.92)                          ▼ (Similarity < 0.92)
           CACHE HIT (~5ms)                                CACHE MISS (~1000ms)
       Return Cached LLM Response                        Call LLM Engine -> Store in Cache
```

### Benefits & Risks

- **Latency Reduction:** Drops latency from $\sim 1500\text{ ms}$ to $< 10\text{ ms}$.
- **Cost Reduction:** Reduces API provider billing by $30\% - 60\%$ in high-traffic enterprise applications.
- **Cache Staleness Risk:** If underlying knowledge changes, stale cached responses can be served unless cache invalidation TTLs are configured.

## Example

Conceptual Python snippet using similarity threshold for semantic caching:

```python
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_cached_response(query_vec, cache_db, threshold=0.92):
    for cached_query_vec, cached_response in cache_db:
        sim = cosine_similarity(query_vec, cached_query_vec)
        if sim >= threshold:
            return cached_response, sim
    return None, 0.0
```

## Interview tips

- Discuss setting the similarity threshold: setting it too high ($>0.98$) leads to low hit rates; setting it too low ($<0.85$) risks returning responses for unrelated user questions.
- Explain cache tenant isolation: ensuring cached data from Tenant A is never returned to Tenant B.

---

[⬅ Back to AI System Design](./README.md) · [All topics](../README.md)
