---
title: "What is single-representation vs multi-representation document retrieval?"
id: 124
category: "RAG and Vector Databases"
difficulty: "Beginner"
tags:
  - ai-engineering
  - rag-and-vector-databases
  - interview-questions
---

# What is single-representation vs multi-representation document retrieval?

**Short answer:** Single-representation retrieval embeds an entire document chunk into a single vector embedding; multi-representation retrieval decouples the search index from the generation context, generating multiple distinct vector summaries or synthetic questions for search while linking back to full raw document chunks.

## Detail

In standard single-representation RAG, text chunks are embedded directly:

```text
Single-Representation: [Raw 500-Word Chunk] ──► Embed ──► Single Vector in Index
```

If a document chunk contains multiple dense ideas, a single vector embedding dilutes specific detail signals.

```text
Multi-Representation:  [Raw 500-Word Chunk] ──┬──► Generate Summary ──► Vector A (Index)
                                              ├──► Generate Questions ──► Vector B (Index)
                                              └──► Raw Full Text (Retrieved for Prompt Context)
```

### Advantages of Multi-Representation Retrieval

1. **Question-to-Question Matching:** Embedding synthetic questions generated from text aligns closely with user query vector structures.
2. **Context Preservation:** Short summaries yield precise vector matches, but the LLM receives the full raw parent document during generation.

## Example

Python concept mapping multiple search vectors to a parent document:

```python
class MultiRepresentationDocStore:
    def __init__(self):
        self.doc_store = {} # parent_id -> full raw document text
        self.vector_index = [] # tuples of (vector, parent_id)

    def add_document(self, parent_id: str, raw_text: str, summary_vec, questions_vec):
        self.doc_store[parent_id] = raw_text
        # Both vectors link to the same parent document ID
        self.vector_index.append((summary_vec, parent_id))
        self.vector_index.append((questions_vec, parent_id))
```

## Interview tips

- Connect multi-representation indexing to Parent-Document Retriever patterns in LangChain/LlamaIndex.
- Highlight how multi-representation RAG solves table and code snippet retrieval bottlenecks.

## Related Concepts

- [[How does Parent-Document Retrieval link fine-grained vector chunks back to full parent context?]] (`#126`): [How does Parent-Document Retrieval link fine-grained vector chunks back to full parent context?](../rag-and-vector-databases/how-does-parent-document-retrieval-link-fine-grained-vector-chunks-back-to-full-parent-context.md)
- [[How does RAPTOR perform hierarchical tree-organized retrieval?]] (`#129`): [How does RAPTOR perform hierarchical tree-organized retrieval?](../rag-and-vector-databases/how-does-raptor-perform-hierarchical-tree-organized-retrieval.md)
- [[How to build an automated RAG evaluation harness measuring Context Precision and Recall?]] (`#178`): [How to build an automated RAG evaluation harness measuring Context Precision and Recall?](../evaluation-and-testing/how-to-build-an-automated-rag-evaluation-harness-measuring-context-precision-and-recall.md)

---

[⬅ Back to RAG and Vector Databases](./README.md) · [All topics](../README.md)
