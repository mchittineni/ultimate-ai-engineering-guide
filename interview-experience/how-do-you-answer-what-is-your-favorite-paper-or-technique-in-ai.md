---
title: "How do you answer 'What is your favorite paper or technique in AI'?"
id: 99
category: "Interview Experience"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - interview-experience
  - interview-questions
---

# How do you answer 'What is your favorite paper or technique in AI'?

**Short answer:** Structure your answer by clearly naming the paper/technique (e.g. FlashAttention, LoRA, DPO, GRPO/DeepSeek R1), explaining the core technical problem it solved, detailing the mathematical or architectural mechanism, and highlighting how you applied its principles in your own production projects.

## Detail

Interviewers use this question to test whether you actively keep up with state-of-the-art AI research and understand the practical engineering implications of recent papers.

### The 4-Part Response Blueprint

```
1. Selection & Thesis  ──► Name paper/technique (e.g. FlashAttention-2 or DPO)
2. The Bottleneck      ──► What was broken before? (HBM memory traffic vs quadratic attention)
3. The Core Mechanism  ──► How does it work under the hood? (Tiling online softmax / logit ratios)
4. Production Impact   ──► How did it impact your work or modern AI systems?
```

### High-Impact Papers to Draw From

- **FlashAttention (Dao et al.):** Tiling GPU SRAM to eliminate HBM IO bottlenecks.
- **LoRA (Hu et al.):** Low-rank matrix decomposition for efficient parameter adaptation.
- **DPO (Rafailov et al.):** Eliminating reward models in preference alignment.
- **DeepSeek-R1 (DeepSeek Team):** GRPO relative group rewards driving reasoning emergence without explicit teacher traces.

## Example

Sample answer outline for **Group Relative Policy Optimization (GRPO)**:

```markdown
- **Thesis:** "My favorite recent paper is DeepSeek-R1, specifically the GRPO alignment mechanism."
- **Bottleneck:** "PPO in traditional RLHF requires running policy, reference, value (critic), and reward models concurrently, consuming massive GPU VRAM."
- **Mechanism:** "GRPO eliminates the critic model entirely by sampling a group of G outputs per prompt and calculating relative baseline advantages normalized against the group reward mean and standard deviation."
- **Impact:** "This enabled scaling RL directly on rule-based verifiers (math compilers and unit tests), allowing reasoning behaviors to emerge natively."
```

## Interview tips

- Pick a paper you genuinely understand deeply; interviewers will follow up with mathematical or implementation questions.
- Connect the paper's theoretical contribution directly to real-world inference or training efficiency.

---

[⬅ Back to Interview Experience](./README.md) · [All topics](../README.md)
