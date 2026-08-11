---
title: "How does contextual compression reduce context window token usage during RAG?"
id: 128
category: "RAG and Vector Databases"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - rag-and-vector-databases
  - interview-questions
---

# How does contextual compression reduce context window token usage during RAG?

**Short answer:** Contextual compression parses retrieved document chunks and strips out irrelevant sentences, fluff, or non-matching paragraphs before assembling the LLM prompt context window, reducing prompt token costs and latency while eliminating context clutter.

## Detail

Vector search retrieves full document chunks (e.g. 500 tokens). Often, only a single 20-token sentence within a 500-token chunk directly answers the user's prompt.

```text
Retrieved Raw Chunks: [500 Tokens Chunk A] + [500 Tokens Chunk B] = 1000 Prompt Tokens
                                         │
                                         ▼
Contextual Compressor:  Strips irrelevant sentences relative to user query
                                         │
                                         ▼
Compressed Context:   [30 Tokens relevant from A] + [25 Tokens relevant from B] = 55 Tokens
```

### Compression Techniques

1. **LLM Sentence Extractor:** Using a fast model (e.g. `gpt-4o-mini`) to extract query-relevant sentences from retrieved chunks.
2. **Embeddings Filter:** Splitting retrieved chunks into individual sentences, computing similarity against the user query, and discarding low-similarity sentences.

## Example

Python concept illustrating embedding-based sentence compression:

```python
def compress_context_by_sentence(query_vec: list[float], chunk_text: str, embedder_fn, threshold: float = 0.6) -> str:
    sentences = [s.strip() for s in chunk_text.split(".") if s.strip()]
    relevant_sentences = []

    for sent in sentences:
        sent_vec = embedder_fn(sent)
        sim = float(sum(q * s for q, s in zip(query_vec, sent_vec))) # Cosine sim
        if sim >= threshold:
            relevant_sentences.append(sent)

    return ". ".join(relevant_sentences) + "."
```

## Interview tips

- Highlight latency trade-offs: contextual compression adds minor processing latency before the main LLM call, but saves token costs and improves generation precision.
- Connect contextual compression to solving the "Lost in the Middle" phenomenon.

## Related Concepts

- [[What is context window truncation and how do you handle overflow gracefully?]] (`#115`): [What is context window truncation and how do you handle overflow gracefully?](../prompt-engineering/what-is-context-window-truncation-and-how-do-you-handle-overflow-gracefully.md)
- [[What is prefix caching (prompt caching) and how does it eliminate redundant KV computation?]] (`#152`): [What is prefix caching (prompt caching) and how does it eliminate redundant KV computation?](../ai-system-design/what-is-prefix-caching-prompt-caching-and-how-does-it-eliminate-redundant-kv-computation.md)
- [[How to build an automated RAG evaluation harness measuring Context Precision and Recall?]] (`#178`): [How to build an automated RAG evaluation harness measuring Context Precision and Recall?](../evaluation-and-testing/how-to-build-an-automated-rag-evaluation-harness-measuring-context-precision-and-recall.md)

---

[⬅ Back to RAG and Vector Databases](./README.md) · [All topics](../README.md)
