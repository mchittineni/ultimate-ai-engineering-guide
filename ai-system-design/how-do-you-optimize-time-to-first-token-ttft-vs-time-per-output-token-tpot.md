---
title: "How do you optimize Time to First Token (TTFT) vs Time Per Output Token (TPOT)?"
id: 7
category: "AI System Design"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - ai-system-design
  - interview-questions
---

# How do you optimize Time to First Token (TTFT) vs Time Per Output Token (TPOT)?

**Short answer:** Time to First Token (TTFT) measures prompt prefill latency (compute-bound), while Time Per Output Token (TPOT) measures streaming generation speed per token (memory-bandwidth bound); optimizing each requires distinct architectural strategies.

## Detail

In production LLM serving, user-perceived responsiveness depends on two core SLA metrics:

1. **TTFT (Time to First Token):** The time elapsed between sending a user request and receiving the very first streamed token. It includes prompt tokenization, routing, KV cache allocation, and running the compute-bound prefill forward pass over all prompt tokens.
2. **TPOT (Time Per Output Token):** The average time spent generating each subsequent token during the decoding phase. It measures how fast text streams across the user's screen (inverse of Tokens Per Second per user).

```text
User Clicks Send ───► [Prefill Phase] ───► First Token Received ───► [Decoding Phase] ───► Generation Complete
                       │                   │                          │
                       └───── TTFT ────────┘                          └─── TPOT ──────────┘
```

### Architectural Trade-offs & Optimizations

| Latency Metric | Bound Type             | Primary Bottleneck                                      | Optimization Strategies                                                                                                                                                                                                            |
| -------------- | ---------------------- | ------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **TTFT**       | Compute Bound          | GPU Tensor Core Matrix Multiply FLOPs (Prompt Length)   | - **Chunked Prefill:** Split long prompts into smaller blocks.<br>- **Prompt Caching:** Reuse precomputed KV cache for static system prompts.<br>- **Prefix Tuning & FlashAttention.**                                             |
| **TPOT**       | Memory Bandwidth Bound | HBM Memory Transfer Speed (Fetching weights + KV cache) | - **PagedAttention (vLLM):** Eliminate KV cache fragmentation.<br>- **Speculative Decoding:** Use a small draft model to generate tokens in parallel.<br>- **Weight Quantization (INT8/INT4):** Reduce bytes transferred per step. |

### Disaggregation (Prefill-Decode Disaggregation)

Modern production clusters (like Mooncake or Splitwise architectures) separate GPU worker pools into dedicated **Prefill Nodes** (optimized for compute FLOPs and compute-bound matrix multiplies) and **Decode Nodes** (optimized for memory bandwidth and low-latency KV cache fetches), transferring the KV cache state over high-speed NVLink / InfiniBand.

## Example

Measuring TTFT and TPOT in a Python client streaming API:

```python
import time
from openai import OpenAI

client = OpenAI()

start_time = time.perf_counter()
first_token_time = None
token_timestamps = []

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Explain KV Caching in detail."}],
    stream=True
)

for chunk in response:
    if chunk.choices[0].delta.content:
        now = time.perf_counter()
        if first_token_time is None:
            first_token_time = now
            ttft = first_token_time - start_time
            print(f"TTFT: {ttft * 1000:.2f} ms")
        token_timestamps.append(now)

# Calculate TPOT
if len(token_timestamps) > 1:
    total_decoding_time = token_timestamps[-1] - first_token_time
    output_tokens = len(token_timestamps)
    tpot = (total_decoding_time / (output_tokens - 1)) * 1000
    print(f"TPOT: {tpot:.2f} ms/token ({1000/tpot:.2f} tokens/sec)")
```

## Interview tips

- Always explain why prefill is compute-bound: all $N$ prompt tokens go through in one pass, so each weight load from HBM is amortized across $N$ tokens ($O(N)$ FLOPs in the linear layers, $O(N^2)$ in attention) — high arithmetic intensity, tensor cores saturated. Decoding is memory-bandwidth bound because each sequential step reloads the full weight set to produce a single token.
- Mention Chunked Prefills (Sarathi/vLLM) as the solution to prevent long prompt prefills from starving ongoing decode streams (eliminating tail latency spikes).

---

[⬅ Back to AI System Design](./README.md) · [All topics](../README.md)
