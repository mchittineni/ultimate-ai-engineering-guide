---
title: "How does PagedAttention in vLLM solve memory fragmentation?"
id: 33
category: "AI System Design"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - ai-system-design
  - interview-questions
---

# How does PagedAttention in vLLM solve memory fragmentation?

**Short answer:** PagedAttention partitions the LLM Key-Value (KV) cache into fixed-size physical memory blocks and uses a virtual memory lookup table—similar to OS virtual memory paging—allowing KV cache memory to be allocated dynamically in non-contiguous physical GPU space with near 0% memory waste.

## Detail

In traditional inference servers (e.g. HuggingFace Transformers), KV memory must be pre-allocated contiguously for every incoming request based on its maximum potential sequence length (e.g., 4096 tokens).

### The Problem: Virtual Memory Fragmentation

1. **Over-reservation:** Allocating 4K contiguous slots when a request generates only 100 tokens wastes $>90\%$ of VRAM.
2. **External Fragmentation:** Dynamic allocation/deallocation creates fragmented physical memory holes.
3. **Low Batch Size:** Due to VRAM waste, servers can only process small batch sizes ($B=4$ or $8$), bottlenecking serving throughput.

### The PagedAttention Solution

```text
Logical KV Cache (Tokens 0..15) ──► Block Table Lookup ──► Physical GPU Memory Blocks
   Block 0 (Tokens 0-3)    ─────────────► Physical Block 12
   Block 1 (Tokens 4-7)    ─────────────► Physical Block 3
   Block 2 (Tokens 8-11)   ─────────────► Physical Block 87
```

- KV cache for a sequence is split into physical blocks holding $N$ tokens (e.g. 16 tokens).
- As sequence length grows token-by-token, new physical blocks are allocated on demand.
- Multiple requests (or parallel beam searches) can share physical memory blocks safely (copy-on-write).

## Example

Python block mapping table concept:

```python
class PagedKVCacheManager:
    def __init__(self, block_size=16, total_gpu_blocks=1024):
        self.block_size = block_size
        self.free_blocks = list(range(total_gpu_blocks))
        self.block_tables = {} # req_id -> list of block indices

    def allocate_slot(self, req_id: str, seq_len: int):
        num_blocks_needed = (seq_len + self.block_size - 1) // self.block_size
        if req_id not in self.block_tables:
            self.block_tables[req_id] = []

        while len(self.block_tables[req_id]) < num_blocks_needed:
            block = self.free_blocks.pop(0)
            self.block_tables[req_id].append(block)
```

## Interview tips

- Highlight that PagedAttention enables up to $2-4\times$ throughput increases in inference serving engines like vLLM and TensorRT-LLM.
- Mention copy-on-write mechanics for parallel sampling and prompt prefix caching.

---

[⬅ Back to AI System Design](./README.md) · [All topics](../README.md)
