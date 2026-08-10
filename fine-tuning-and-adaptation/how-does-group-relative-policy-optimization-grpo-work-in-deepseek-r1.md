---
title: "How does Group Relative Policy Optimization (GRPO) work in DeepSeek R1?"
id: 30
category: "Fine-Tuning and Adaptation"
difficulty: "Advanced"
tags:
  - ai-engineering
  - fine-tuning-and-adaptation
  - interview-questions
---

# How does Group Relative Policy Optimization (GRPO) work in DeepSeek R1?

**Short answer:** Group Relative Policy Optimization (GRPO) eliminates the memory-intensive critic (value) model in PPO by sampling a group of $G$ outputs for each prompt, evaluating their rewards, and calculating baseline-normalized advantages relative to the group mean and standard deviation.

## Detail

In standard PPO (Proximal Policy Optimization), a critic model of equal size to the policy model must be loaded into GPU memory to estimate the value baseline $V(s)$. For 70B+ parameter models, running policy, reference, value, and reward models concurrently causes extreme VRAM bottlenecks.

### GRPO Mechanism

DeepSeek R1 and DeepSeek Math introduced GRPO to streamline reinforcement learning at scale:

1. **Group Sampling:** For a prompt $q$, sample a group of $G$ outputs $\{o_1, o_2, \dots, o_G\}$ from the old policy $\pi_{\theta_{old}}$.
2. **Reward Calculation:** Compute reward $r_i$ for each output $o_i$ using rule-based verifiers (e.g., math answer correctness, code test cases pass/fail) or reward models.
3. **Relative Advantage Estimation:** Normalize rewards across the sampled group:

$$A_i = \frac{r_i - \text{mean}(\{r_1, \dots, r_G\})}{\text{std}(\{r_1, \dots, r_G\}) + \epsilon}$$

4. **Policy Update:** Optimize policy using clipped surrogate objective with KL divergence penalty against reference model:

$$\mathcal{L}_{GRPO}(\theta) = \frac{1}{G} \sum_{i=1}^{G} \left( \min \left( \frac{\pi_\theta(o_i|q)}{\pi_{\theta_{old}}(o_i|q)} A_i, \text{clip} \left( \frac{\pi_\theta(o_i|q)}{\pi_{\theta_{old}}(o_i|q)}, 1-\epsilon, 1+\epsilon \right) A_i \right) - \beta D_{KL}(\pi_\theta || \pi_{ref}) \right)$$

### Why GRPO Enabled DeepSeek R1 Reasoning Emergence

GRPO scales RL training efficiently by allowing reward signals to stem directly from verifiable outcomes (math/code compilers). Over thousands of GRPO steps, models naturally learn long Chain-of-Thought reasoning, self-correction, and verification behaviors without requiring human-annotated reasoning traces.

## Example

Python calculation of GRPO relative group advantage:

```python
import torch

def compute_grpo_advantages(rewards: torch.Tensor, eps: float = 1e-8) -> torch.Tensor:
    # rewards shape: [batch_size, group_size G]
    mean = rewards.mean(dim=-1, keepdim=True)
    std = rewards.std(dim=-1, keepdim=True)
    advantages = (rewards - mean) / (std + eps)
    return advantages

# Sample 4 outputs for 1 prompt with binary verifier rewards:
sample_rewards = torch.tensor([[1.0, 0.0, 0.0, 1.0]]) # 2 correct, 2 failed
advantages = compute_grpo_advantages(sample_rewards)
print("GRPO Relative Advantages:", advantages)
```

## Interview tips

- Highlight that GRPO removes the critic model, reducing RL training memory requirements by $\sim 50\%$.
- Emphasize how rule-based verifiers (unit tests, math string matching) replace subjective human reward models in GRPO reasoning pipelines.

---

[⬅ Back to Fine-Tuning and Adaptation](./README.md) · [All topics](../README.md)
