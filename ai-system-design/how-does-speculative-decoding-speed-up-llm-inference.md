---
title: "How does speculative decoding speed up LLM inference?"
id: 34
category: "AI System Design"
difficulty: "Advanced"
tags:
  - ai-engineering
  - ai-system-design
  - interview-questions
---

# How does speculative decoding speed up LLM inference?

**Short answer:** Speculative decoding pairs a small, fast draft model with a large target LLM; the draft model quickly predicts $K$ candidate tokens sequentially, and the target LLM validates all $K$ tokens simultaneously in a single parallel forward pass, achieving $2-3\times$ latency reduction without altering output quality.

## Detail

Standard autoregressive generation is strictly memory-bandwidth bound: generating 1 token requires loading all 70B parameters from HBM into SRAM ($O(W)$ memory transfer for a single token forward pass).

### Speculative Decoding Pipeline

```
[Draft Model (Drafts K=5 tokens)] ──► [ "The", "quick", "brown", "fox", "jumps" ] (Fast sequential)
                                                     │
[Target Model (Parallel Pass)]   ──► Verifies all K candidate tokens in 1 forward pass
                                                     │
[Accept / Reject Gate]           ──► Accepts 4 tokens + samples 1 new token -> Move forward
```

1. **Draft Generation:** A fast draft model (e.g. 1B parameter model) generates $K$ draft tokens sequentially.
2. **Target Validation:** The target model (e.g. 70B model) processes all $K$ tokens concurrently in a single batch forward pass, computing target token distributions.
3. **Acceptance Criterion:** Modified rejection sampling accepts candidate tokens matching target model probabilities. If candidate $i$ is rejected, remaining candidates are discarded, and target model resamples token $i$.

### Speedup Ratio

Because computing $K$ tokens in parallel takes nearly the same time as 1 forward pass on high-bandwidth GPUs, accepting $M \le K$ tokens per step yields significant wall-clock speedup ($2\times - 3.5\times$).

## Example

Python conceptual representation of Speculative Decoding loop:

```python
def speculative_decoding_step(draft_model, target_model, context, K=4):
    # Step 1: Draft K tokens rapidly
    draft_tokens = draft_model.generate(context, max_new_tokens=K)
    
    # Step 2: Target model evaluates all K tokens in parallel (1 forward pass)
    target_logits = target_model.forward(context + draft_tokens)
    
    accepted_tokens = []
    for i, token in enumerate(draft_tokens):
        if target_logits[i].argmax() == token: # Simplified acceptance
            accepted_tokens.append(token)
        else:
            # Resample from target model on first mismatch
            accepted_tokens.append(target_logits[i].argmax())
            break
            
    return accepted_tokens
```

## Interview tips

- Emphasize that speculative decoding produces **mathematically identical** output sampling distributions as calling the target LLM alone.
- Note alternative draft generation methods: Medusa heads (adding multi-head draft predictions on top of the target model itself without needing a separate draft model).

---

[⬅ Back to AI System Design](./README.md) · [All topics](../README.md)
