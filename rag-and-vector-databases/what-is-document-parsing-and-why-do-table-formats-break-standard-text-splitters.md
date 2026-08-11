---
title: "What is document parsing and why do table formats break standard text splitters?"
id: 125
category: "RAG and Vector Databases"
difficulty: "Beginner"
tags:
  - ai-engineering
  - rag-and-vector-databases
  - interview-questions
---

# What is document parsing and why do table formats break standard text splitters?

**Short answer:** Document parsing extracts text, tables, images, and layout hierarchy from complex files (PDFs, DOCX); standard text splitters break tables because naive character/token chunking slices through table rows and columns, severing column headers from data values.

## Detail

PDF documents store visual rendering instructions, not structured text grids.

```text
PDF Raw Rendering Stream:  "Sales" (x=100, y=500), "$4.2M" (x=300, y=500)
Naive Character Chunker:   Slices at character 500 ──► Separates "$4.2M" from "Sales" header
```

### Why Naive Chunking Destroys Table Semantics

1. **Header Loss:** Slicing a 50-row table into 500-token chunks isolates row 40 from column header definitions at row 1.
2. **Column Misalignment:** Extracting PDF text line-by-line reads left-to-right across columns, merging adjacent table cells into nonsensical sentences.

### Modern Document Parsing Solutions

- **Vision-Based Document Layout Parsers:** (e.g. Unstructured, LlamaParse, Marker) utilizing vision models to reconstruct HTML/Markdown table structures prior to chunking.
- **Table-to-Markdown Transformation:** Converting financial tables to explicit Markdown (`| Header 1 | Header 2 |`) or JSON strings before embedding.

## Example

Python concept transforming raw table rows into self-contained key-value strings:

```python
def serialize_table_rows(headers: list[str], rows: list[list[str]]) -> list[str]:
    # Ensure every chunked row retains column header context
    serialized_chunks = []
    for row in rows:
        row_str = ", ".join(f"{h}: {v}" for h, v in zip(headers, row))
        serialized_chunks.append(row_str)
    return serialized_chunks

headers = ["Quarter", "Revenue", "Margin"]
row = ["Q3 2024", "$12.4M", "24%"]
print("Serialized Table Row Chunk:", serialize_table_rows(headers, [row]))
```

## Interview tips

- Highlight that garbage-in-garbage-out during document parsing is responsible for over 60% of enterprise RAG failure cases.
- Discuss multi-modal document processing (passing PDF page screenshots directly to Multimodal Vision LLMs).

## Related Concepts

- [[What is single-representation vs multi-representation document retrieval?]] (`#124`): [What is single-representation vs multi-representation document retrieval?](../rag-and-vector-databases/what-is-single-representation-vs-multi-representation-document-retrieval.md)
- [[What is indirect prompt injection and how does it occur when parsing web pages/documents?]] (`#181`): [What is indirect prompt injection and how does it occur when parsing web pages/documents?](../ai-safety-and-governance/what-is-indirect-prompt-injection-and-how-does-it-occur-when-parsing-web-pages-documents.md)
- [[How to conduct a complete system design interview for a multi-tenant enterprise RAG search platform?]] (`#199`): [How to conduct a complete system design interview for a multi-tenant enterprise RAG search platform?](../interview-experience/how-to-conduct-a-complete-system-design-interview-for-a-multi-tenant-enterprise-rag-search-platform.md)

---

[⬅ Back to RAG and Vector Databases](./README.md) · [All topics](../README.md)
