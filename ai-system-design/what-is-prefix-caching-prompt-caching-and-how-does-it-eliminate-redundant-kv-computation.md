---
title: "What is prefix caching (prompt caching) and how does it eliminate redundant KV computation?"
id: 152
category: "AI System Design"
difficulty: "Beginner"
tags:
  - ai-engineering
  - ai-system-design
  - interview-questions
---

# What is prefix caching (prompt caching) and how does it eliminate redundant KV computation?

**Short answer:** Prefix caching (prompt caching) stores precomputed Key-Value (KV) tensors for frequently reused initial prompt prefixes (such as long system prompts, few-shot exemplars, or standard document context) in GPU memory, skipping prefill matrix operations for matching prefixes and reducing Time-to-First-Token (TTFT) by up to 80%.

## Detail

In multi-turn chat applications or RAG pipelines, every incoming API request re-sends the same system instructions.

```text
Request 1: [System Prompt (2000 Tokens)] + [User Query 1] ──► Full Prefill Computation ──► Cache KV Tensors
Request 2: [System Prompt (2000 Tokens)] + [User Query 2] ──► PREFIX CACHE HIT! Read KV ──► Only Prefill Query 2
```

### Mechanics of Prefix Caching

1. **Token Hash Indexing:** The inference engine (vLLM / SGLang / Anthropic API) hashes token sequences in blocks (e.g. 16 or 64 tokens).
2. **KV Tensor Lookup:** Incoming prompt prefix hashes are checked against active GPU KV cache memory pages.
3. **Prefill Bypass:** Matched prefix blocks bypass self-attention prefill computation entirely.

## Example

Conceptual Python prefix cache lookup dictionary:

```python
import hashlib

class PrefixKVCacheManager:
    def __init__(self):
        self.cache = {} # prefix_hash -> kv_tensor_page_id

    def get_or_compute_kv(self, prefix_tokens: list[int], compute_fn):
        prefix_bytes = str(prefix_tokens).encode()
        prefix_hash = hashlib.sha256(prefix_bytes).hexdigest()

        if prefix_hash in self.cache:
            print("PREFIX CACHE HIT! Reusing precomputed KV tensors.")
            return self.cache[prefix_hash]

        print("PREFIX CACHE MISS. Executing prefill matrix multiplication...")
        kv_tensors = compute_fn(prefix_tokens)
        self.cache[prefix_hash] = kv_tensors
        return kv_tensors
```

## Interview tips

- Highlight latency and cost savings: Anthropic and OpenAI offer prompt caching API discounts (e.g. 50–90% cost reduction for cached prompt tokens).
- Connect prefix caching to PagedAttention virtual block memory management.

## Related Concepts

- [[How does Parent-Document Retrieval link fine-grained vector chunks back to full parent context?]] (`#126`): [How does Parent-Document Retrieval link fine-grained vector chunks back to full parent context?](../rag-and-vector-databases/how-does-parent-document-retrieval-link-fine-grained-vector-chunks-back-to-full-parent-context.md)
- [[How does vLLM PagedAttention manage Virtual Memory Pages to eliminate KV cache fragmentation?]] (`#159`): [How does vLLM PagedAttention manage Virtual Memory Pages to eliminate KV cache fragmentation?](../ai-system-design/how-does-vllm-pagedattention-manage-virtual-memory-pages-to-eliminate-kv-cache-fragmentation.md)

---

[⬅ Back to AI System Design](./README.md) · [All topics](../README.md)
