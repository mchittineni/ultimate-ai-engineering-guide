---
title: "LLM Fundamentals"
category: "LLM Fundamentals"
tags:
  - ai-engineering
  - llm-fundamentals
  - index
---

# LLM Fundamentals

Core architectures, Transformer mechanics, self-attention, context windows, tokenization, KV cache, and sampling algorithms.

**20 questions** · 🟢 Beginner: 10 · 🟡 Intermediate: 6 · 🔴 Advanced: 4

## Questions

| #   | Question                                                                                                                                                                             | Difficulty      |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------- |
| 1   | [What is KV Cache and how does it speed up inference?](./what-is-kv-cache-and-how-does-it-speed-up-inference.md)                                                                     | 🟡 Intermediate |
| 2   | [How does Grouped-Query Attention (GQA) differ from Multi-Head Attention (MHA)?](./how-does-grouped-query-attention-gqa-differ-from-multi-head-attention-mha.md)                     | 🟡 Intermediate |
| 12  | [What is the difference between encoder-only, decoder-only, and encoder-decoder LLMs?](./what-is-the-difference-between-encoder-only-decoder-only-and-encoder-decoder-llms.md)       | 🟢 Beginner     |
| 13  | [How does Byte-Pair Encoding (BPE) tokenization work?](./how-does-byte-pair-encoding-bpe-tokenization-work.md)                                                                       | 🟢 Beginner     |
| 14  | [How do Rotary Position Embeddings (RoPE) and RoPE scaling work?](./how-do-rotary-position-embeddings-rope-and-rope-scaling-work.md)                                                 | 🔴 Advanced     |
| 51  | [What is Temperature, Top-p, and Top-k sampling?](./what-is-temperature-top-p-and-top-k-sampling.md)                                                                                 | 🟢 Beginner     |
| 52  | [What is the difference between greedy decoding and beam search?](./what-is-the-difference-between-greedy-decoding-and-beam-search.md)                                               | 🟢 Beginner     |
| 53  | [What is a context window and how does it limit LLM processing?](./what-is-a-context-window-and-how-does-it-limit-llm-processing.md)                                                 | 🟢 Beginner     |
| 54  | [How does Multi-Query Attention (MQA) differ from Multi-Head Attention?](./how-does-multi-query-attention-mqa-differ-from-multi-head-attention.md)                                   | 🟡 Intermediate |
| 55  | [How does FlashAttention optimize memory and speed via tiling?](./how-does-flashattention-optimize-memory-and-speed-via-tiling.md)                                                   | 🔴 Advanced     |
| 101 | [What is tokenization and why can't LLMs process raw string characters directly?](./what-is-tokenization-and-why-cant-llms-process-raw-string-characters-directly.md)                | 🟢 Beginner     |
| 102 | [What is the difference between causal and bidirectional self-attention?](./what-is-the-difference-between-causal-and-bidirectional-self-attention.md)                               | 🟢 Beginner     |
| 103 | [What is a logit and how is it converted to token probabilities via Softmax?](./what-is-a-logit-and-how-is-it-converted-to-token-probabilities-via-softmax.md)                       | 🟢 Beginner     |
| 104 | [What is an attention mask and why is it needed during batch processing?](./what-is-an-attention-mask-and-why-is-it-needed-during-batch-processing.md)                               | 🟢 Beginner     |
| 105 | [What is positional encoding and why do Transformers need it?](./what-is-positional-encoding-and-why-do-transformers-need-it.md)                                                     | 🟢 Beginner     |
| 106 | [How do Mixture of Experts (MoE) architectures scale parameter count efficiently?](./how-do-mixture-of-experts-moe-architectures-scale-parameter-count-efficiently.md)               | 🟡 Intermediate |
| 107 | [What is linear attention and how does it attempt to solve quadratic complexity?](./what-is-linear-attention-and-how-does-it-attempt-to-solve-quadratic-complexity.md)               | 🟡 Intermediate |
| 108 | [How does sliding window attention (SWA) reduce memory usage in long-context models?](./how-does-sliding-window-attention-swa-reduce-memory-usage-in-long-context-models.md)         | 🟡 Intermediate |
| 109 | [How do state space models (SSMs) like Mamba compare to Transformer self-attention?](./how-do-state-space-models-ssms-like-mamba-compare-to-transformer-self-attention.md)           | 🔴 Advanced     |
| 110 | [How does Differential Attention work to suppress noise and improve long-context focus?](./how-does-differential-attention-work-to-suppress-noise-and-improve-long-context-focus.md) | 🔴 Advanced     |

## What interviewers probe here

- Explain scaled dot-product attention and QKV projection math.
- Trade-offs between autoregressive (decoder-only) vs encoder-decoder models.
- How KV caching eliminates redundant recomputation during inference.

---

[⬅ Back to all topics](../README.md)
