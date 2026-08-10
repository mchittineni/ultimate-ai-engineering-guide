---
title: "How does chunked prefill disaggregate prefill and decoding nodes?"
id: 80
category: "AI System Design"
difficulty: "Advanced"
tags:
  - ai-engineering
  - ai-system-design
  - interview-questions
---

# How does chunked prefill disaggregate prefill and decoding nodes?

**Short answer:** Chunked prefill splits long prompt prefill processing into smaller token chunks that are interleaved into autoregressive decoding batches; disaggregated prefill/decoding separates inference infrastructure onto dedicated GPU clusters optimized specifically for prefill FLOP compute vs decoding memory bandwidth.

## Detail

In standard inference engines (e.g. vLLM), prompt prefill and token decoding run on the same GPUs.

When a 10,000-token prompt arrives, it preempts active token decoding streams, causing severe spike latency in Time-Per-Output-Token (TPOT) for concurrent users.

```text
Unified Nodes (Interference):
[Decode Stream] ──► [LONG PREFILL (10K Tokens) PREEMPTS GPU] ──► [TPOT Spike ~500ms]

Disaggregated Architecture (DistServe / Mooncake):
[Prefill GPU Cluster (Compute-Heavy)] ──► Computes Prompt KV ──► Transfer KV over RDMA
                                                                     │
[Decode GPU Cluster (Memory-Heavy)]  ◄───────────────────────────────┘
```

### Architectural Advancements

1. **Chunked Prefill (Sarathi / vLLM):** Large prompts are broken into chunks (e.g. 512 tokens). Each chunk is piggybacked alongside active decoding steps, smoothing out TPOT spikes.
2. **Disaggregated Prefill-Decode (P&D):**
   - **Prefill Instances:** Optimized for high compute (FLOPs) and tensor parallelism.
   - **Decode Instances:** Optimized for memory bandwidth and high batch capacity.
   - **KV Transfer:** Precomputed KV tensors are transferred from prefill nodes to decode nodes over high-speed RDMA / PCIe interconnects.

## Example

Python concept illustrating chunked prefill interleaving:

```python
def interleave_chunked_prefill(prompt_tokens: list[int], active_decode_reqs: list[dict], chunk_size: int = 512):
    # Split 2048 token prompt into 4 x 512 chunks
    chunks = [prompt_tokens[i : i + chunk_size] for i in range(0, len(prompt_tokens), chunk_size)]

    execution_steps = []
    for chunk in chunks:
        # Step combines 1 prefill chunk + 1 decode step for all active streams
        step_payload = {
            "prefill_chunk_len": len(chunk),
            "num_active_decodes": len(active_decode_reqs)
        }
        execution_steps.append(step_payload)
    return execution_steps
```

## Interview tips

- Emphasize that disaggregation eliminates inter-phase interference, keeping TPOT stable under heavy prompt loads.
- Discuss RDMA network transfer bandwidth requirements when transmitting multi-gigabyte KV caches across GPU nodes.

---

[⬅ Back to AI System Design](./README.md) · [All topics](../README.md)
