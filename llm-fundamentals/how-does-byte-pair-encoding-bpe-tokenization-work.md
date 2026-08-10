---
title: "How does Byte-Pair Encoding (BPE) tokenization work?"
id: 13
category: "LLM Fundamentals"
difficulty: "Beginner"
tags:
  - ai-engineering
  - llm-fundamentals
  - interview-questions
---

# How does Byte-Pair Encoding (BPE) tokenization work?

**Short answer:** Byte-Pair Encoding (BPE) is a subword tokenization algorithm that begins with individual characters (or bytes) and iteratively merges the most frequently adjacent pairs of tokens in a corpus until a predefined vocabulary size is reached.

## Detail

Tokenization translates raw text strings into numeric token IDs that LLMs can process. BPE balances vocabulary size and sequence length by finding frequent character patterns.

### The Training Phase

1. **Initialization:** Split raw text into individual characters (e.g., `'h'`, `'e'`, `'l'`, `'l'`, `'o'`) and build a base vocabulary.
2. **Frequency Counting:** Count all adjacent symbol pairs in the training corpus.
3. **Merging:** Identify the most frequent pair (e.g., `'e'` + `'r'` $\rightarrow$ `'er'`), add the merged token to the vocabulary, and update all occurrences in the corpus.
4. **Iteration:** Repeat until reaching the target vocabulary size (e.g., 32,000 for Llama 2 or 128,000 for Llama 3).

### Modern Byte-Level BPE (tiktoken)

Modern LLM tokenizers (such as OpenAI's `tiktoken`) use byte-level BPE, initializing the vocabulary with 256 raw byte values. This guarantees that any UTF-8 string can be tokenized without encountering out-of-vocabulary (OOV) tokens.

## Example

Python demonstration of a basic BPE merge step:

```python
from collections import Counter

def get_stats(vocab):
    pairs = Counter()
    for word, freq in vocab.items():
        symbols = word.split()
        for i in range(len(symbols) - 1):
            pairs[symbols[i], symbols[i+1]] += freq
    return pairs

# Corpus vocabulary representation: word -> frequency
vocab = {'l o w </w>': 5, 'l o w e r </w>': 2, 'n e w e s t </w>': 6}
pairs = get_stats(vocab)
most_frequent = max(pairs, key=pairs.get)

print("Most frequent adjacent pair to merge:", most_frequent)
```

## Interview tips

- Mention tokenization edge cases: non-English languages and code often tokenize into more tokens per word, increasing latency and API costs.
- Note how BPE affects arithmetic performance (e.g., numbers being tokenized into irregular digit chunks).

---

[⬅ Back to LLM Fundamentals](./README.md) · [All topics](../README.md)
