---
title: "How to detect semantic drift in user queries using embedding clustering over time?"
id: 167
category: "LLMOps and Production AI"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - llmops-and-production-ai
  - interview-questions
---

# How to detect semantic drift in user queries using embedding clustering over time?

**Short answer:** Semantic drift detection embeds incoming user queries, clusters vector representations over sliding time windows (e.g. daily vs monthly), and calculates vector distribution shifts (such as Fréchet Distance or Cosine Centroid Distance) to identify emerging user topics, unexpected queries, or out-of-domain prompt shifts.

## Detail

Over time, production user prompt distributions drift away from initial benchmark datasets due to new product releases, seasonal trends, or changed user habits.

```
Time Window T1 (Baseline):  [Cluster A: Billing], [Cluster B: Login Issues]
                                        │
                                        ▼ (Compute Centroid Distance)
Time Window T2 (Current):   [Cluster A: Billing], [NEW Emerging Cluster C: Feature X Bug]
```

### Detection Metrics

1. **Centroid Distance Shift:** Computing cosine distance between the mean vector of baseline queries $\mu_1$ and active queries $\mu_2$:

$$d_{drift} = 1 - \cos(\mu_1, \mu_2)$$

2. **Unassigned Vector Rate:** Tracking the percentage of production query vectors falling outside pre-established HDBSCAN cluster boundaries.

## Example

Python semantic drift detection concept:

```python
import numpy as np

def calculate_centroid_drift(baseline_embeddings: np.ndarray, current_embeddings: np.ndarray) -> float:
    # Compute mean centroid vectors
    c_base = np.mean(baseline_embeddings, axis=0)
    c_curr = np.mean(current_embeddings, axis=0)
    
    # Cosine distance
    cosine_sim = np.dot(c_base, c_curr) / (np.linalg.norm(c_base) * np.linalg.norm(c_curr))
    drift = 1.0 - cosine_sim
    return float(drift)

# Simulate two embedding arrays
base_vecs = np.random.randn(100, 1536)
curr_vecs = np.random.randn(100, 1536) + 0.5 # Shift distribution
print(f"Detected Semantic Drift Score: {calculate_centroid_drift(base_vecs, curr_vecs):.4f}")
```

## Interview tips

- Explain how detecting semantic drift triggers automated golden dataset updates and prompt fine-tuning.
- Connect semantic drift detection to production observability platforms like Arize and Phoenix.

## Related Concepts

- [[What is an embedding model and how does vector dimension affect search quality?]] (`#121`): [What is an embedding model and how does vector dimension affect search quality?](../rag-and-vector-databases/what-is-an-embedding-model-and-how-does-vector-dimension-affect-search-quality.md)
- [[How to build a continuous evaluation pipeline sampling production traces for human review?]] (`#168`): [How to build a continuous evaluation pipeline sampling production traces for human review?](../llmops-and-production-ai/how-to-build-a-continuous-evaluation-pipeline-sampling-production-traces-for-human-review.md)
- [[How to build an automated RAG evaluation harness measuring Context Precision and Recall?]] (`#178`): [How to build an automated RAG evaluation harness measuring Context Precision and Recall?](../evaluation-and-testing/how-to-build-an-automated-rag-evaluation-harness-measuring-context-precision-and-recall.md)

---

[⬅ Back to LLMOps and Production AI](./README.md) · [All topics](../README.md)
