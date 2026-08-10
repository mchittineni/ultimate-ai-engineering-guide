---
title: "How does query rewriting and Hypothetical Document Embeddings (HyDE) work?"
id: 64
category: "RAG and Vector Databases"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - rag-and-vector-databases
  - interview-questions
---

# How does query rewriting and Hypothetical Document Embeddings (HyDE) work?

**Short answer:** Query rewriting transforms vague user queries into clear, expanded search terms; Hypothetical Document Embeddings (HyDE) uses an LLM to generate a zero-shot fake "ideal response" document, embedding that hypothetical text to search vector databases for real documents matching its semantic pattern.

## Detail

Directly embedding brief user queries (e.g. _"Why is my server slow?"_) often results in poor vector matches because query syntax differs structurally from document syntax.

### HyDE Pipeline

```text
[User Query] ──► [LLM Generator] ──► [Hypothetical Answer Document]
                                                │
                                                ▼
[Vector DB]  ◄── [Embedding Match] ◄── [Embed Hypothetical Doc]
```

1. **Hypothetical Generation:** The LLM generates a plausible hypothetical document answering the query without accessing external DBs.
2. **Embedding & Search:** The hypothetical text is converted to a vector embedding. Because answer-to-answer embeddings align closer in vector space than query-to-answer embeddings, search precision improves.
3. **Real Document Retrieval:** The vector DB returns actual grounded documents matching the hypothetical structure.

## Example

Python concept illustrating HyDE workflow:

```python
def hyde_retrieval(user_query: str, llm_fn, embedder_fn, vector_db):
    # Step 1: Generate hypothetical document
    hyde_prompt = f"Write a detailed passage answering the question: '{user_query}'"
    hypothetical_doc = llm_fn(hyde_prompt)

    # Step 2: Embed hypothetical doc instead of short user query
    hypothetical_vector = embedder_fn(hypothetical_doc)

    # Step 3: Perform vector search using hypothetical vector
    real_documents = vector_db.search(hypothetical_vector, k=5)
    return real_documents
```

## Interview tips

- Note that HyDE introduces additional latency (one extra LLM call prior to retrieval).
- Explain when HyDE excels (complex, open-ended conceptual queries) vs when it fails (exact keyword / SKU part searches).

---

[⬅ Back to RAG and Vector Databases](./README.md) · [All topics](../README.md)
