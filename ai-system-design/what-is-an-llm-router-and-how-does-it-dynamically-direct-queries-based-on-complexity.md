---
title: "What is an LLM router and how does it dynamically direct queries based on complexity?"
id: 153
category: "AI System Design"
difficulty: "Beginner"
tags:
  - ai-engineering
  - ai-system-design
  - interview-questions
---

# What is an LLM router and how does it dynamically direct queries based on complexity?

**Short answer:** An LLM router evaluates incoming user prompts (using lightweight classification models, intent embeddings, or rule-based heuristics) to dynamically route low-complexity queries to fast, cheap models (e.g. GPT-4o-mini) and high-complexity queries to frontier reasoning models (e.g. o3-mini or GPT-4o), reducing overall API costs by 60–80%.

## Detail

Routing 100% of user queries to frontier flagship models causes excessive cost and unnecessary latency.

```text
Incoming User Query
         │
         ▼
[LLM Router (Intent / Embedding Classifier)]
         │
         ├─► Simple Q&A / Classification ──► Route to `gpt-4o-mini` / `llama-3-8b` ($0.15 / 1M tokens)
         │
         └─► Complex Math / Code Generation ──► Route to `o3-mini` / `gpt-4o` ($5.00 / 1M tokens)
```

### Routing Mechanisms

1. **Lightweight Classification Model:** A fast BERT or 1B model trained to categorize intent (`simple`, `coding`, `reasoning`).
2. **Embedding Distance Router:** Measuring cosine similarity between query embeddings and exemplar cluster vectors for different complexity tiers.
3. **Cascade Routing (Fallback):** Attempting completion on a small cheap model first; if quality evaluation checks fail, falling back to a larger model.

## Example

Python concept illustrating intent-based LLM routing:

```python
def route_user_query(prompt: str) -> str:
    COMPLEX_KEYWORDS = {"code", "python", "refactor", "proof", "math", "architect"}
    words = set(prompt.lower().split())

    # Check if query contains high-complexity technical triggers
    if words.intersection(COMPLEX_KEYWORDS) or len(prompt.split()) > 200:
        return "models/flagship-reasoning-model" # High complexity -> Route to o3-mini / GPT-4o

    return "models/lightweight-fast-model" # Low complexity -> Route to GPT-4o-mini

print("Routing Simple Query:", route_user_query("What is the capital of France?"))
print("Routing Complex Query:", route_user_query("Write a Python script to compute async graph deadlocks."))
```

## Interview tips

- Discuss RouteLLM (open-source benchmark and routing library).
- Emphasize tracking accuracy vs cost Pareto frontiers when tuning router confidence thresholds.

## Related Concepts

- [[How does Directional Stimulus Prompting guide LLMs toward specific output aspects?]] (`#116`): [How does Directional Stimulus Prompting guide LLMs toward specific output aspects?](../prompt-engineering/how-does-directional-stimulus-prompting-guide-llms-toward-specific-output-aspects.md)
- [[What is load balancing for LLM inference clusters across multi-region GPU pools?]] (`#151`): [What is load balancing for LLM inference clusters across multi-region GPU pools?](../ai-system-design/what-is-load-balancing-for-llm-inference-clusters-across-multi-region-gpu-pools.md)
- [[How to design an enterprise-grade LLM Gateway with dynamic fallback, tenant rate limiting, and cost allocation?]] (`#169`): [How to design an enterprise-grade LLM Gateway with dynamic fallback, tenant rate limiting, and cost allocation?](../llmops-and-production-ai/how-to-design-an-enterprise-grade-llm-gateway-with-dynamic-fallback-tenant-rate-limiting-and-cost-allocation.md)

---

[⬅ Back to AI System Design](./README.md) · [All topics](../README.md)
