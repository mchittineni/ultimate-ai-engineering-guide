---
title: "How does ORPO perform SFT and alignment in a single step without reference models?"
id: 149
category: "Fine-Tuning and Adaptation"
difficulty: "Advanced"
tags:
  - ai-engineering
  - fine-tuning-and-adaptation
  - interview-questions
---

# How does ORPO perform SFT and alignment in a single step without reference models?

**Short answer:** ORPO (Monolithic Odds Ratio Preference Optimization) combines Supervised Fine-Tuning (SFT) cross-entropy loss with an odds ratio penalty term in a single unified loss function, aligning model preferences toward winning completions without requiring a separate reference model or dedicated DPO/RLHF phase.

## Detail

Traditional preference alignment requires a 2-stage pipeline:

1. Stage 1: Supervised Fine-Tuning (SFT) on target dataset.
2. Stage 2: Preference alignment (DPO or RLHF), requiring loading both policy model $\pi_\theta$ and frozen reference model $\pi_{ref}$ into GPU memory simultaneously.

```text
Standard 2-Stage DPO: SFT Training ──► Save Checkpoint ──► Load Policy + Reference Models into VRAM ──► DPO Loss
ORPO Single-Stage:   Raw Base Model ──► Monolithic ORPO Loss (SFT Loss + Odds Ratio Penalty) ──► Aligned Model
```

### The ORPO Loss Function

$$\mathcal{L}_{ORPO} = \mathcal{L}_{SFT} + \lambda \cdot \mathcal{L}_{OR}$$

Where:

- $\mathcal{L}_{SFT}$ is standard negative log-likelihood on favored completions $y_w$.
- $\mathcal{L}_{OR}$ is the log odds ratio between winning $y_w$ and losing $y_l$ completions:

$$\text{Odds}(y|x) = \frac{P_\theta(y|x)}{1 - P_\theta(y|x)}$$

$$\mathcal{L}_{OR} = -\log \sigma \left( \log \frac{\text{Odds}(y_w|x)}{\text{Odds}(y_l|x)} \right)$$

## Example

PyTorch implementation concept for ORPO Loss:

```python
import torch
import torch.nn.functional as F

def orpo_loss(policy_chosen_logps, policy_rejected_logps, sft_loss, lambda_or=0.1):
    # Calculate log odds ratio
    log_odds_chosen = policy_chosen_logps - torch.log1p(-torch.exp(policy_chosen_logps))
    log_odds_rejected = policy_rejected_logps - torch.log1p(-torch.exp(policy_rejected_logps))

    log_odds_ratio = log_odds_chosen - log_odds_rejected
    or_loss = -F.logsigmoid(log_odds_ratio).mean()

    # Unified monolithic loss
    total_loss = sft_loss + lambda_or * or_loss
    return total_loss
```

## Interview tips

- Emphasize memory efficiency: ORPO eliminates the reference model, saving ~50% GPU VRAM during preference alignment compared to DPO.
- Highlight that ORPO prevents preference alignment degradation while accelerating training throughput.

## Related Concepts

- [[What is dataset formatting for instruction tuning (Alpaca vs ShareGPT formats)?]] (`#141`): [What is dataset formatting for instruction tuning (Alpaca vs ShareGPT formats)?](../fine-tuning-and-adaptation/what-is-dataset-formatting-for-instruction-tuning-alpaca-vs-sharegpt-formats.md)
- [[How does DoRA (Weight-Decomposed Low-Rank Adaptation) improve directional weight updates over LoRA?]] (`#146`): [How does DoRA (Weight-Decomposed Low-Rank Adaptation) improve directional weight updates over LoRA?](../fine-tuning-and-adaptation/how-does-dora-weight-decomposed-low-rank-adaptation-improve-directional-weight-updates-over-lora.md)
- [[What is human evaluation (RLHF human rating) and how do you design annotation rubrics?]] (`#175`): [What is human evaluation (RLHF human rating) and how do you design annotation rubrics?](../evaluation-and-testing/what-is-human-evaluation-rlhf-human-rating-and-how-do-you-design-annotation-rubrics.md)

---

[⬅ Back to Fine-Tuning and Adaptation](./README.md) · [All topics](../README.md)
