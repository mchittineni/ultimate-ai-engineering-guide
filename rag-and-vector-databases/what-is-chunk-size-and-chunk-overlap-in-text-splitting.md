---
title: "What is chunk size and chunk overlap in text splitting?"
id: 61
category: "RAG and Vector Databases"
difficulty: "Beginner"
tags:
  - ai-engineering
  - rag-and-vector-databases
  - interview-questions
---

# What is chunk size and chunk overlap in text splitting?

**Short answer:** Chunk size defines the maximum token/character length of individual text segments extracted from large documents for embedding; chunk overlap specifies the number of shared tokens/characters between adjacent chunks to prevent context fragmentation across boundaries.

## Detail

Vector embedding models have fixed context windows (e.g. 512 tokens for `bge-large-en` or 8192 tokens for `text-embedding-3-small`). Long documents (PDFs, Markdown files) must be segmented prior to indexing.

```
Document Text: [==================================================]
Chunk 1:       [===============>]
Chunk 2:               [<Overlap>]===============>]
```

### Trade-offs

| Parameter | Low Value Impact | High Value Impact |
| --- | --- | --- |
| **Chunk Size** | Fine-grained precision, but loses broader document context | Richer context, but higher embedding noise and LLM prompt context cost |
| **Chunk Overlap** | Faster indexing, but risks splitting sentences/facts mid-thought | Preserves context across boundaries, but creates duplicate vector storage |

Standard baseline starting point: 512 tokens chunk size with 10–15% overlap (50–75 tokens).

## Example

Python sliding window text chunker implementation with overlap:

```python
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    tokens = text.split()
    chunks = []
    step = chunk_size - overlap
    for i in range(0, len(tokens), step):
        chunk = " ".join(tokens[i : i + chunk_size])
        chunks.append(chunk)
        if i + chunk_size >= len(tokens):
            break
    return chunks

doc = "Word " * 1200
chunks = chunk_text(doc, chunk_size=500, overlap=50)
print(f"Generated {len(chunks)} chunks with 50-word overlap.")
```

## Interview tips

- Mention semantic chunking (splitting text dynamically by paragraph or markdown headers) over naive character splitters.
- Explain how small chunks excel at precise retrieval while parent-document retrieval links small retrieved chunks back to full parent sections.

---

[⬅ Back to RAG and Vector Databases](./README.md) · [All topics](../README.md)
