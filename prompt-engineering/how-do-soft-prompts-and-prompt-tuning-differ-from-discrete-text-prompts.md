---
title: "How do soft prompts and prompt tuning differ from discrete text prompts?"
id: 120
category: "Prompt Engineering"
difficulty: "Advanced"
tags:
  - ai-engineering
  - prompt-engineering
  - interview-questions
---

# How do soft prompts and prompt tuning differ from discrete text prompts?

**Short answer:** Discrete text prompts consist of human-readable string tokens mapped to fixed vocabulary embedding entries; soft prompts (Prefix Tuning) consist of continuous, trainable vector tensors Prepended directly to LLM key/value or embedding matrices, optimized via backpropagation while keeping base model weights frozen.

## Detail

Discrete prompt engineering operates exclusively in human natural language space:

```text
Discrete Prompt: "Summarize this text: " ──► Tokenizer ──► Embedding Lookup (Fixed Vectors)
Soft Prompt:     [Trainable Tensor P_1, P_2, ... P_k] ──► Prepended directly to Transformer Hidden States
```

### Key Differences

| Dimension              | Discrete Text Prompts                           | Soft Prompts (Prompt Tuning)                                         |
| ---------------------- | ----------------------------------------------- | -------------------------------------------------------------------- |
| **Representation**     | Human-readable strings ("You are an expert...") | Continuous un-interpretable vector tensors $\mathbb{R}^{K \times d}$ |
| **Optimization**       | Trial-and-error, manual edits, LLM-search       | Backpropagation via loss gradient descent ($\nabla_\theta L$)        |
| **Model Weight State** | Frozen                                          | Base model frozen; Soft prompt parameters trained                    |
| **Deployment**         | Passed as text tokens in API prompt             | Injected into GPU tensor forward pass                                |

## Example

PyTorch implementation concept prepending a soft prompt tensor to input embeddings:

```python
import torch
import torch.nn as nn

class SoftPromptWrapper(nn.Module):
    def __init__(self, base_embedding_layer, soft_prompt_length=10, embedding_dim=4096):
        super().__init__()
        self.embedding = base_embedding_layer
        # Trainable soft prompt parameters
        self.soft_prompt = nn.Parameter(torch.randn(1, soft_prompt_length, embedding_dim) * 0.01)

    def forward(self, input_ids):
        # 1. Lookup discrete token embeddings
        token_embeds = self.embedding(input_ids)
        # 2. Prepend continuous soft prompt vectors
        full_embeds = torch.cat([self.soft_prompt.repeat(input_ids.size(0), 1, 1), token_embeds], dim=1)
        return full_embeds
```

## Interview tips

- Highlight that soft prompt tuning requires open-weight model access to compute gradients over embeddings (unsupported on closed APIs like OpenAI).
- Explain how soft prompts enable Parameter-Efficient Fine-Tuning (PEFT) with ultra-small parameter footprints (a few kilobytes).

## Related Concepts

- [[What is weight merging in LoRA and why does it eliminate inference latency penalties?]] (`#145`): [What is weight merging in LoRA and why does it eliminate inference latency penalties?](../fine-tuning-and-adaptation/what-is-weight-merging-in-lora-and-why-does-it-eliminate-inference-latency-penalties.md)
- [[How does DoRA (Weight-Decomposed Low-Rank Adaptation) improve directional weight updates over LoRA?]] (`#146`): [How does DoRA (Weight-Decomposed Low-Rank Adaptation) improve directional weight updates over LoRA?](../fine-tuning-and-adaptation/how-does-dora-weight-decomposed-low-rank-adaptation-improve-directional-weight-updates-over-lora.md)
- [[How to answer scenario questions about trade-offs between RAG and Fine-Tuning?]] (`#194`): [How to answer scenario questions about trade-offs between RAG and Fine-Tuning?](../interview-experience/how-to-answer-scenario-questions-about-trade-offs-between-rag-and-fine-tuning.md)

---

[⬅ Back to Prompt Engineering](./README.md) · [All topics](../README.md)
