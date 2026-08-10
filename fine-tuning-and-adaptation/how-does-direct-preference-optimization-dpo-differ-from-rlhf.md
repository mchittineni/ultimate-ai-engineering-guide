---
title: "How does Direct Preference Optimization (DPO) differ from RLHF?"
id: 29
category: "Fine-Tuning and Adaptation"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - fine-tuning-and-adaptation
  - interview-questions
---

# How does Direct Preference Optimization (DPO) differ from RLHF?

**Short answer:** Reinforcement Learning from Human Feedback (RLHF) trains a separate reward model on pairwise preferences and uses PPO to optimize the policy model; Direct Preference Optimization (DPO) mathematically reparameterizes the reward function, directly optimizing policy model weights on preference pairs using a binary cross-entropy loss without training a separate reward model or running complex PPO reinforcement learning.

## Detail

Aligning LLMs with human preferences (Helpful, Harmless, Honest) traditionally required standard RLHF (e.g. InstructGPT):

### Traditional RLHF Pipeline

1. **SFT (Supervised Fine-Tuning):** Train baseline policy $\pi^{SFT}$.
2. **Reward Model Training:** Train reward model $R_\psi(x, y)$ on preferred ($y_w$) vs dispreferred ($y_l$) completions.
3. **PPO Optimization:** Optimize policy $\pi_\theta$ using PPO against $R_\psi$ with a KL divergence penalty to avoid drifting from $\pi^{SFT}$.

### DPO Simplification

DPO proves that the optimal policy solution can be expressed directly as a function of the log ratio of policy probabilities:

$$\mathcal{L}_{DPO}(\theta; \pi_{ref}) = -\mathbb{E}_{(x, y_w, y_l)} \left[ \log \sigma \left( \beta \log \frac{\pi_\theta(y_w|x)}{\pi_{ref}(y_w|x)} - \beta \log \frac{\pi_\theta(y_l|x)}{\pi_{ref}(y_l|x)} \right) \right]$$

Where:

- $y_w$ is the winning (preferred) response, $y_l$ is the losing (dispreferred) response.
- $\pi_\theta$ is the policy model being trained; $\pi_{ref}$ is the frozen reference SFT model.
- $\beta$ is a hyperparameter scaling KL divergence penalty.

| Feature                   | RLHF (PPO)                                    | DPO                                              |
| ------------------------- | --------------------------------------------- | ------------------------------------------------ |
| **Reward Model Required** | Yes (Separate model in VRAM)                  | No                                               |
| **Training Stability**    | Unstable (Sensitive to PPO hyperparameters)   | Extremely Stable (Supervised cross-entropy loss) |
| **GPU Memory Footprint**  | Very High (Policy, Reference, Reward, Critic) | Moderate (Policy + Reference)                    |

## Example

PyTorch implementation of DPO loss function:

```python
import torch
import torch.nn.functional as F

def dpo_loss(policy_win_logps, policy_lose_logps, ref_win_logps, ref_lose_logps, beta=0.1):
    policy_logratios = policy_win_logps - policy_lose_logps
    ref_logratios = ref_win_logps - ref_lose_logps

    logits = policy_logratios - ref_logratios
    losses = -F.logsigmoid(beta * logits)
    return losses.mean()
```

## Interview tips

- Highlight that DPO eliminated PPO instability, making preference alignment dramatically easier and accessible on smaller GPU clusters.
- Mention variations like KTO (Kahneman-Tversky Optimization) and ORPO (Odds Ratio Preference Optimization).

---

[⬅ Back to Fine-Tuning and Adaptation](./README.md) · [All topics](../README.md)
