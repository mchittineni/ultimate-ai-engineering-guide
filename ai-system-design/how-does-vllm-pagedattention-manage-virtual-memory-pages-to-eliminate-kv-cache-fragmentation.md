---
title: "How does vLLM PagedAttention manage Virtual Memory Pages to eliminate KV cache fragmentation?"
id: 159
category: "AI System Design"
difficulty: "Advanced"
tags:
  - ai-engineering
  - ai-system-design
  - interview-questions
---

# How does vLLM PagedAttention manage Virtual Memory Pages to eliminate KV cache fragmentation?

**Short answer:** PagedAttention manages KV cache memory by partitioning key and value tensors into fixed-size physical memory blocks (pages) mapped via a virtual page table, eliminating contiguous VRAM pre-allocation and reducing memory waste from ~60-80% down to under 4%.

## Detail

Traditional inference engines pre-allocate contiguous GPU memory blocks for every request based on `max_context_length` (e.g. 4096 tokens).

Because actual generated sequences vary in length, pre-allocating contiguous blocks causes severe **internal and external memory fragmentation**:

```
Traditional KV Allocator (Contiguous Allocation):
[ Req 1 (Reserved 4096 Tokens) | Actual Output: 100 Tokens | 3996 Tokens WASTED ] ──► ~80% VRAM Wasted!

PagedAttention (Virtual Block Mapping):
Virtual Pages:  [Block 0] ──► Physical GPU Memory Block 42 (Non-contiguous, 16 Tokens)
                [Block 1] ──► Physical GPU Memory Block 105 (Non-contiguous, 16 Tokens)
(Memory allocated dynamically on-demand per 16-token page)
```

### Key Technical Innovations in PagedAttention

1. **Virtual Block Tables:** Maps logical sequence token blocks to non-contiguous physical GPU VRAM blocks (inspired by OS Virtual Memory).
2. **Dynamic Page Allocation:** Allocates 1 block (e.g. 16 tokens) at a time as generation proceeds.
3. **Copy-on-Write Memory Sharing:** Enables multiple request streams (e.g. parallel sampling or tree search) to share physical KV memory blocks for identical prompt prefixes.

## Example

Python concept illustrating virtual-to-physical block mapping in PagedAttention:

```python
class PagedKVCacheManager:
    def __init__(self, block_size=16, total_gpu_blocks=1000):
        self.block_size = block_size
        self.free_blocks = list(range(total_gpu_blocks))
        self.block_tables = {} # seq_id -> list of physical block IDs

    def allocate_token_slot(self, seq_id: str, current_seq_len: int) -> int:
        if seq_id not in self.block_tables:
            self.block_tables[seq_id] = []
            
        # Check if new physical block is needed
        if current_seq_len % self.block_size == 1:
            physical_block = self.free_blocks.pop(0)
            self.block_tables[seq_id].append(physical_block)
            
        return self.block_tables[seq_id][-1]
```

## Interview tips

- Highlight that PagedAttention allows serving $2-4\times$ larger batch sizes on the same GPU hardware compared to traditional engines.
- Connect PagedAttention to prefix caching and parallel beam search efficiency.

## Related Concepts

- [[What is prefix caching (prompt caching) and how does it eliminate redundant KV computation?]] (`#152`): [What is prefix caching (prompt caching) and how does it eliminate redundant KV computation?](../ai-system-design/what-is-prefix-caching-prompt-caching-and-how-does-it-eliminate-redundant-kv-computation.md)
- [[How does Chunked Prefill prevent decoding latency spikes during concurrent batch processing?]] (`#156`): [How does Chunked Prefill prevent decoding latency spikes during concurrent batch processing?](../ai-system-design/how-does-chunked-prefill-prevent-decoding-latency-spikes-during-concurrent-batch-processing.md)

---

[⬅ Back to AI System Design](./README.md) · [All topics](../README.md)
