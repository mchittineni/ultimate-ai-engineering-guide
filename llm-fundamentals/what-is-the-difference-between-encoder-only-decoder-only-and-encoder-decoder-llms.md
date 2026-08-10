---
title: "What is the difference between encoder-only, decoder-only, and encoder-decoder LLMs?"
id: 12
category: "LLM Fundamentals"
difficulty: "Beginner"
tags:
  - ai-engineering
  - llm-fundamentals
  - interview-questions
---

# What is the difference between encoder-only, decoder-only, and encoder-decoder LLMs?

**Short answer:** Encoder-only models (e.g., BERT) process bidirectional context to extract rich vector representations for classification and extraction; decoder-only models (e.g., GPT-4, Llama) use causal masking to generate text token-by-token; encoder-decoder models (e.g., T5) process a full input sequence into representations and autoregressively decode a target output sequence.

## Detail

Transformer architectures differ primarily in how attention masks are applied across sequence tokens:

| Architecture        | Attention Mechanism                                                     | Key Use Cases                                                                       | Representative Models         |
| ------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------------- |
| **Encoder-Only**    | Bidirectional (every token attends to every token)                      | Sentence embeddings, search ranking, classification, Named Entity Recognition (NER) | BERT, RoBERTa, DeBERTa        |
| **Decoder-Only**    | Causal / Unidirectional (tokens attend only to past and current tokens) | Open-ended text generation, chat, code generation, reasoning                        | GPT-4, Llama 3, Mistral, Qwen |
| **Encoder-Decoder** | Bidirectional in encoder, causal in decoder + cross-attention           | Sequence-to-sequence translation, summarization, doc parsing                        | T5, BART, Whisper             |

### Why Decoder-Only Predominates Modern Generative AI

While encoder-decoder models were initially favored for translation, decoder-only models scale more efficiently for general zero-shot and few-shot task performance. Pre-training a massive decoder-only model on next-token prediction enables implicit learning of classification, translation, summarization, and reasoning within a single unified architecture.

## Example

Below is a conceptual PyTorch snippet illustrating how attention masks differ between encoder and decoder models:

```python
import torch

seq_len = 4
# Encoder: Unmasked bidirectional self-attention
encoder_mask = torch.ones((seq_len, seq_len))

# Decoder: Causal triangular mask preventing access to future tokens
decoder_mask = torch.tril(torch.ones((seq_len, seq_len)))

print("Encoder Attention Mask:\n", encoder_mask)
print("\nDecoder Attention Mask:\n", decoder_mask)
```

## Interview tips

- Emphasize that modern LLM applications predominantly use decoder-only architectures, whereas dense retrieval embedding models for RAG typically rely on encoder-only architectures.
- Mention cross-attention as the key mechanism connecting the encoder outputs to the decoder in sequence-to-sequence models like T5.

---

[⬅ Back to LLM Fundamentals](./README.md) · [All topics](../README.md)
