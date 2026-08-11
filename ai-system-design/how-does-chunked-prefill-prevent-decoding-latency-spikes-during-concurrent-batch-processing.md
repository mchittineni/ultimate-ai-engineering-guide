---
title: "How does Chunked Prefill prevent decoding latency spikes during concurrent batch processing?"
id: 156
category: "AI System Design"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - ai-system-design
  - interview-questions
---

# How does Chunked Prefill prevent decoding latency spikes during concurrent batch processing?

**Short answer:** Chunked Prefill splits long prompt prefill token sequences into smaller chunks (e.g. 512 tokens), interleaving these prefill chunks alongside ongoing autoregressive token decoding steps in the same batch, preventing long prefill requests from monopolizing GPU compute and causing Time-Per-Output-Token (TPOT) latency spikes.

## Detail

In standard inference engines without chunked prefill, a new request with a 10,000-token prompt preempts active decoding requests, running compute-heavy matrix multiplications across all 10,000 tokens in a single pass.

```
Without Chunked Prefill (Interference Spike):
Active Decode Streams ──► [LONG PREFILL (10,000 Tokens) BLOCKS GPU] ──► TPOT Spikes to 500ms+

With Chunked Prefill (Sarathi / vLLM):
Step 1: Batch = [Prefill Chunk 1 (512 tokens)] + [Active Decodes (1 token each)] -> Latency ~30ms
Step 2: Batch = [Prefill Chunk 2 (512 tokens)] + [Active Decodes (1 token each)] -> Latency ~30ms
```

### Architectural Mechanics

1. **Max Budget Allocation:** Setting a maximum token budget per batch iteration (e.g. 4096 tokens total per iteration).
2. **Dynamic Interleaving:** Combining $M$ active decoding tokens with $N$ prompt prefill tokens to hit the target FLOP saturation point.
3. **TPOT Stability:** Keeps token decoding latency smooth and predictable under heavy concurrent user loads.

## Example

Python concept illustrating batch budget calculation for chunked prefill:

```python
def assemble_chunked_batch(prefill_queue: list[list[int]], active_decodes: list[int], max_num_batched_tokens: int = 2048):
    batch_tokens = []
    
    # 1. Allocate 1 token slot for each active decoding stream
    num_decodes = len(active_decodes)
    remaining_budget = max_num_batched_tokens - num_decodes
    
    # 2. Fill remaining token budget with prompt prefill chunks
    prefill_chunk_size = 0
    if prefill_queue and remaining_budget > 0:
        next_prompt = prefill_queue[0]
        prefill_chunk_size = min(len(next_prompt), remaining_budget)
        
    return {
        "num_decodes": num_decodes,
        "prefill_chunk_size": prefill_chunk_size,
        "total_batch_tokens": num_decodes + prefill_chunk_size
    }
```

## Interview tips

- Emphasize that chunked prefill is a key feature in modern inference engines like vLLM and TGI.
- Connect chunked prefill to prefill/decoding disaggregation.

## Related Concepts

- [[How does vLLM PagedAttention manage Virtual Memory Pages to eliminate KV cache fragmentation?]] (`#159`): [How does vLLM PagedAttention manage Virtual Memory Pages to eliminate KV cache fragmentation?](../ai-system-design/how-does-vllm-pagedattention-manage-virtual-memory-pages-to-eliminate-kv-cache-fragmentation.md)

---

[⬅ Back to AI System Design](./README.md) · [All topics](../README.md)
