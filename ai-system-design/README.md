---
title: "AI System Design"
category: "AI System Design"
tags:
  - ai-engineering
  - ai-system-design
  - index
---

# AI System Design

High-throughput inference, TTFT/TPOT, streaming (SSE), semantic caching, GPU resource planning, and serving infrastructure (vLLM, TGI).

**20 questions** · 🟢 Beginner: 10 · 🟡 Intermediate: 6 · 🔴 Advanced: 4

## Questions

| #   | Question                                                                                                                                                                                                                         | Difficulty      |
| --- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 7   | [How do you optimize Time to First Token (TTFT) vs Time Per Output Token (TPOT)?](./how-do-you-optimize-time-to-first-token-ttft-vs-time-per-output-token-tpot.md)                                                               | 🟡 Intermediate |
| 31  | [What is Server-Sent Events (SSE) streaming for LLM responses?](./what-is-server-sent-events-sse-streaming-for-llm-responses.md)                                                                                                 | 🟢 Beginner     |
| 32  | [How does semantic caching reduce LLM API latency and cost?](./how-does-semantic-caching-reduce-llm-api-latency-and-cost.md)                                                                                                     | 🟢 Beginner     |
| 33  | [How does PagedAttention in vLLM solve memory fragmentation?](./how-does-pagedattention-in-vllm-solve-memory-fragmentation.md)                                                                                                   | 🟡 Intermediate |
| 34  | [How does speculative decoding speed up LLM inference?](./how-does-speculative-decoding-speed-up-llm-inference.md)                                                                                                               | 🔴 Advanced     |
| 76  | [What is continuous batching and how does it improve GPU utilization?](./what-is-continuous-batching-and-how-does-it-improve-gpu-utilization.md)                                                                                 | 🟢 Beginner     |
| 77  | [What is the difference between prefill phase and decoding phase?](./what-is-the-difference-between-prefill-phase-and-decoding-phase.md)                                                                                         | 🟢 Beginner     |
| 78  | [What is GPU VRAM bandwidth and why is decoding memory-bound?](./what-is-gpu-vram-bandwidth-and-why-is-decoding-memory-bound.md)                                                                                                 | 🟢 Beginner     |
| 79  | [How do you design a multi-tenant LLM gateway with rate limits?](./how-do-you-design-a-multi-tenant-llm-gateway-with-rate-limits.md)                                                                                             | 🟡 Intermediate |
| 80  | [How does chunked prefill disaggregate prefill and decoding nodes?](./how-does-chunked-prefill-disaggregate-prefill-and-decoding-nodes.md)                                                                                       | 🔴 Advanced     |
| 151 | [What is load balancing for LLM inference clusters across multi-region GPU pools?](./what-is-load-balancing-for-llm-inference-clusters-across-multi-region-gpu-pools.md)                                                         | 🟢 Beginner     |
| 152 | [What is prefix caching (prompt caching) and how does it eliminate redundant KV computation?](./what-is-prefix-caching-prompt-caching-and-how-does-it-eliminate-redundant-kv-computation.md)                                     | 🟢 Beginner     |
| 153 | [What is an LLM router and how does it dynamically direct queries based on complexity?](./what-is-an-llm-router-and-how-does-it-dynamically-direct-queries-based-on-complexity.md)                                               | 🟢 Beginner     |
| 154 | [What is connection pooling and keep-alive strategy for high-throughput LLM streaming APIs?](./what-is-connection-pooling-and-keep-alive-strategy-for-high-throughput-llm-streaming-apis.md)                                     | 🟢 Beginner     |
| 155 | [What is graceful degradation in AI services when model providers experience downtime?](./what-is-graceful-degradation-in-ai-services-when-model-providers-experience-downtime.md)                                               | 🟢 Beginner     |
| 156 | [How does Chunked Prefill prevent decoding latency spikes during concurrent batch processing?](./how-does-chunked-prefill-prevent-decoding-latency-spikes-during-concurrent-batch-processing.md)                                 | 🟡 Intermediate |
| 157 | [How do tensor parallelism (TP) and pipeline parallelism (PP) split large model weights across multi-GPU nodes?](./how-do-tensor-parallelism-tp-and-pipeline-parallelism-pp-split-large-model-weights-across-multi-gpu-nodes.md) | 🟡 Intermediate |
| 158 | [How does Medusa multi-head decoding accelerate inference without a separate draft model?](./how-does-medusa-multi-head-decoding-accelerate-inference-without-a-separate-draft-model.md)                                         | 🟡 Intermediate |
| 159 | [How does vLLM PagedAttention manage Virtual Memory Pages to eliminate KV cache fragmentation?](./how-does-vllm-pagedattention-manage-virtual-memory-pages-to-eliminate-kv-cache-fragmentation.md)                               | 🔴 Advanced     |
| 160 | [How to design a global multi-region AI inference architecture with sub-100ms TTFT SLAs?](./how-to-design-a-global-multi-region-ai-inference-architecture-with-sub-100ms-ttft-slas.md)                                           | 🔴 Advanced     |

## What interviewers probe here

- Optimizing Time to First Token (TTFT) and Time Per Output Token (TPOT).
- PagedAttention, continuous batching, and speculative decoding.
- Designing semantic caching layers to reduce API expenses and latency.

---

[⬅ Back to all topics](../README.md)
