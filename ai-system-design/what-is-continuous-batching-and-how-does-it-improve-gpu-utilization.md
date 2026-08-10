---
title: "What is continuous batching and how does it improve GPU utilization?"
id: 76
category: "AI System Design"
difficulty: "Beginner"
tags:
  - ai-engineering
  - ai-system-design
  - interview-questions
---

# What is continuous batching and how does it improve GPU utilization?"

**Short answer:** Continuous batching (iteration-level batching) dynamically inserts new incoming requests and evicts completed sequences at every decoding iteration step, eliminating GPU idle time caused by static batching where all sequences wait for the longest sequence to finish.

## Detail

In traditional static batching, requests in a batch are processed together. If Request 1 generates 10 tokens and Request 2 generates 500 tokens, the GPU slots for Request 1 sit completely idle for 490 iterations.

```
Static Batching:
Request 1 (10 tokens):  [Generates 10 tokens] ──► [IDLE GPU WAITING................]
Request 2 (500 tokens): [Generates 500 tokens...................................]

Continuous Batching (vLLM / TGI):
Iteration N: [Req 1 Step 10 (Finished -> EVICTED)] ──► Insert New Req 3 Immediately
Iteration N+1: Batch contains active tokens [Req 2 Step 11, Req 3 Step 1]
```

### Key Performance Benefits

- **Near-100% GPU Compute Utilization:** The GPU tensor cores perform matrix multiplications on a full batch of active tokens at every step.
- **Throughput Multiplier:** Increases inference serving throughput by $10x - 20x$ compared to static batching.

## Example

Python conceptual iteration loop for continuous batching:

```python
class ContinuousBatcher:
    def __init__(self, max_batch_size=4):
        self.active_batch = []
        self.max_batch_size = max_batch_size

    def step(self, new_requests: list):
        # 1. Add new incoming requests to fill open batch slots
        while new_requests and len(self.active_batch) < self.max_batch_size:
            self.active_batch.append(new_requests.pop(0))

        # 2. Perform 1 decoding iteration step across all active requests
        completed = []
        for req in self.active_batch:
            req["generated_tokens"] += 1
            if req["generated_tokens"] >= req["max_tokens"]:
                completed.append(req)

        # 3. Evict finished sequences immediately
        for req in completed:
            self.active_batch.remove(req)
```

## Interview tips

- Highlight that continuous batching was popularized by Orca and vLLM serving architectures.
- Explain how continuous batching works in tandem with PagedAttention to allocate memory for incoming sequences dynamically.

---

[⬅ Back to AI System Design](./README.md) · [All topics](../README.md)
