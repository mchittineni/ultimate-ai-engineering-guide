---
title: "What is the difference between prefill phase and decoding phase?"
id: 77
category: "AI System Design"
difficulty: "Beginner"
tags:
  - ai-engineering
  - ai-system-design
  - interview-questions
---

# What is the difference between prefill phase and decoding phase?

**Short answer:** The prefill phase processes the entire incoming input prompt in parallel, computing initial Key-Value (KV) caches (compute-bound); the decoding phase generates new output tokens one-by-one sequentially, updating the KV cache at each step (memory-bandwidth bound).

## Detail

LLM inference execution splits cleanly into two distinct operational phases:

```
[Input Prompt Tokens (N)] ──► Prefill Phase (Parallel, Compute-Bound) ──► Generates Token 1 (TTFT)
                                                                                  │
[Generated Tokens (1..M)] ◄── Decode Phase (Sequential, Memory-Bound) ◄──────────┘ (TPOT)
```

| Dimension | Prefill Phase (Prompt Processing) | Decoding Phase (Token Generation) |
| --- | --- | --- |
| **Execution Style** | Parallel (All input tokens $N$ processed in 1 pass) | Sequential (1 token generated per iteration step) |
| **Primary Metric** | Time-to-First-Token (TTFT) | Time-Per-Output-Token (TPOT) |
| **Hardware Bottleneck** | Compute-bound (FLOPs / Tensor Core execution) | Memory-bandwidth bound (HBM weight transfer) |
| **KV Cache Impact** | Populates initial KV cache vectors for prompt | Appends 1 new K and V vector per step |

## Example

Python conceptual profile breakdown:

```python
def profile_llm_execution(prompt_len: int, gen_len: int):
    # Prefill: Matrix multiplication over prompt_len tokens (High GPU FLOPs)
    prefill_flops = 2 * prompt_len * (70e9) # 70B parameter estimate
    
    # Decode: Memory fetch of 70B weights for gen_len iterations
    decode_memory_transfers = gen_len * (140e9) # 140GB FP16 parameters per token
    
    return prefill_flops, decode_memory_transfers

flops, mem = profile_llm_execution(prompt_len=2048, gen_len=100)
print(f"Prefill FLOPs: {flops:.2e}, Decode Memory Transfers: {mem:.2e} Bytes")
```

## Interview tips

- Highlight that prefill vs decoding disaggregation (running prefill on compute-heavy nodes and decoding on memory-bandwidth heavy nodes) is an advanced infrastructure optimization pattern.
- Connect prefill phase to TTFT and decoding phase to TPOT latency SLAs.

---

[⬅ Back to AI System Design](./README.md) · [All topics](../README.md)
