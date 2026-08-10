---
title: "What is Retrieval-Augmented Generation (RAG) and why is it used?"
id: 19
category: "RAG and Vector Databases"
difficulty: "Beginner"
tags:
  - ai-engineering
  - rag-and-vector-databases
  - interview-questions
---

# What is Retrieval-Augmented Generation (RAG) and why is it used?

**Short answer:** Retrieval-Augmented Generation (RAG) grounds LLM responses by dynamically fetching relevant external documents from a knowledge base at query time and passing them as context into the LLM prompt.

## Detail

LLMs suffer from three core limitations in enterprise settings:
1. **Hallucinations:** Inventing plausible-sounding facts when lacking specific knowledge.
2. **Stale Knowledge Cutoffs:** Inability to access up-to-date real-time data post pre-training.
3. **Lack of Proprietary Context:** Inability to read internal enterprise databases or private documents.

### The RAG Pipeline

1. **Ingestion & Indexing:** Chunk private documents (PDFs, Markdown, DB rows), compute vector embeddings, and store them in a vector database.
2. **Retrieval:** Embed the user query, search the vector DB for top-$K$ semantic matches (using cosine similarity or HNSW index).
3. **Generation:** Augment the system prompt with retrieved context snippets and pass to the LLM to synthesize an accurate answer.

```
[User Query] ──► [Embedder] ──► [Vector DB Search] ──► Top K Snippets
                                                             │
[User Query] + [Top K Snippets] ──► [LLM Generator] ──► [Grounded Response]
```

## Example

Basic Python implementation of RAG context injection:

```python
def rag_prompt_builder(user_query: str, retrieved_snippets: list[str]) -> str:
    context = "\n---\n".join(retrieved_snippets)
    prompt = f"""You are a helpful assistant. Answer the question using ONLY the provided context snippets below.
If the answer cannot be found in the context, respond with "I do not have enough information to answer."

Context:
{context}

Question: {user_query}
Answer:"""
    return prompt
```

## Interview tips

- Emphasize that RAG is much cheaper and faster to update than model fine-tuning when knowledge changes frequently.
- Highlight the trade-off: RAG is limited by context window sizes, retrieval accuracy, and chunking quality.

---

[⬅ Back to RAG and Vector Databases](./README.md) · [All topics](../README.md)
