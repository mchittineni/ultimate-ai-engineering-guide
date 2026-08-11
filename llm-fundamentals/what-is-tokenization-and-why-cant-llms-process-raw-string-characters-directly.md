---
title: "What is tokenization and why can't LLMs process raw string characters directly?"
id: 101
category: "LLM Fundamentals"
difficulty: "Beginner"
tags:
  - ai-engineering
  - llm-fundamentals
  - interview-questions
---

# What is tokenization and why can't LLMs process raw string characters directly?

**Short answer:** Tokenization maps raw text strings into discrete integer token IDs using subword algorithms (e.g. Byte-Pair Encoding); LLMs cannot process raw string characters directly because character-level representations yield excessively long sequence lengths and weak semantic density, while word-level representations create impossibly large vocabulary tables that fail on out-of-vocabulary terms.

## Detail

Neural networks operate on numerical vector tensors, requiring discrete text to be converted into token indices.

```text
Raw Input Text: "AI Engineering"
                      │
                      ▼
Byte-Pair Encoding (BPE) Tokenizer
                      │
                      ▼
Token IDs:          [15496, 21976] ──► Embedding Matrix Lookup (d_model=4096)
```

### Trade-offs: Character vs Word vs Subword Tokenization

| Level                       | Sequence Length          | Vocabulary Size            | Out-of-Vocabulary (OOV)  |
| --------------------------- | ------------------------ | -------------------------- | ------------------------ |
| **Character-level**         | $4\times$ longer context | Extremely Small (~256)     | Zero OOV                 |
| **Word-level**              | Short context            | Unmanageably Large ($1M+$) | High OOV                 |
| **Subword (BPE/WordPiece)** | Optimal context          | Balanced (32K – 128K)      | Zero OOV (Byte fallback) |

## Example

Python subword tokenization example using `tiktoken`:

```python
import tiktoken

tokenizer = tiktoken.get_encoding("cl100k_base")
text = "Tokenization balances vocabulary size and sequence length."

tokens = tokenizer.encode(text)
decoded_words = [tokenizer.decode([t]) for t in tokens]

print("Token IDs:", tokens)
print("Subword Chunks:", decoded_words)
```

## Interview tips

- Discuss Byte-Pair Encoding (BPE) merge rules and how byte-level fallback prevents out-of-vocabulary errors.
- Explain tokenization quirks (e.g. why LLMs struggle with character-counting tasks like "How many r's in strawberry?").

## Related Concepts

- [[How does Byte-Pair Encoding (BPE) tokenization work?]] (`#13`): [How does Byte-Pair Encoding (BPE) tokenization work?](../llm-fundamentals/how-does-byte-pair-encoding-bpe-tokenization-work.md)
- [[What is mixed precision training (FP16 vs BF16) and why is BF16 preferred on modern GPUs?]] (`#144`): [What is mixed precision training (FP16 vs BF16) and why is BF16 preferred on modern GPUs?](../fine-tuning-and-adaptation/what-is-mixed-precision-training-fp16-vs-bf16-and-why-is-bf16-preferred-on-modern-gpus.md)
- [[What is an embedding model and how does vector dimension affect search quality?]] (`#121`): [What is an embedding model and how does vector dimension affect search quality?](../rag-and-vector-databases/what-is-an-embedding-model-and-how-does-vector-dimension-affect-search-quality.md)

---

[⬅ Back to LLM Fundamentals](./README.md) · [All topics](../README.md)
