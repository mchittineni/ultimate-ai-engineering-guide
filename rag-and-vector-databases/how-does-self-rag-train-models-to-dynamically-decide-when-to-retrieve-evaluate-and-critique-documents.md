---
title: "How does Self-RAG train models to dynamically decide when to retrieve, evaluate, and critique documents?"
id: 130
category: "RAG and Vector Databases"
difficulty: "Advanced"
tags:
  - ai-engineering
  - rag-and-vector-databases
  - interview-questions
---

# How does Self-RAG train models to dynamically decide when to retrieve, evaluate, and critique documents?

**Short answer:** Self-RAG (Self-Reflective Retrieval-Augmented Generation) fine-tunes an LLM to generate special reflection tokens (`[Retrieve]`, `[IsRel]`, `[IsSup]`, `[IsUse]`), allowing the model to dynamically decide when external retrieval is necessary, evaluate document relevance, check output grounding, and critique answer quality on-the-fly.

## Detail

Standard RAG pipelines follow fixed execution paths: ALWAYS retrieve $K$ documents for every user query, even if the query is a simple greeting or common knowledge.

```
Standard RAG: User Query ──► ALWAYS Retrieve ──► Generate Answer

Self-RAG:     User Query ──► Generates Token: [Retrieve=Yes/No]
                             ├──► If No  ──► Generate directly from parametric memory
                             └──► If Yes ──► Retrieve Docs ──► Output [IsRel=Relevant]
                                                             ──► Output [IsSup=FullySupported]
```

### Self-RAG Reflection Tokens

- `[Retrieve]`: Values `{Yes, No, Continue}` — Decides if external retrieval is needed.
- `[IsRel]`: Values `{Relevant, Irrelevant}` — Evaluates if retrieved document contains useful context.
- `[IsSup]`: Values `{FullySupported, PartiallySupported, NoSupport}` — Verifies if output text is grounded in retrieved text (hallucination check).
- `[IsUse]`: Values `{5, 4, 3, 2, 1}` — Rates overall utility of generated output.

## Example

Python concept illustrating Self-RAG token-guided routing:

```python
def self_rag_decide_retrieval(model_completion: str) -> bool:
    # Model generates special reflection token at position 0
    if "[Retrieve=Yes]" in model_completion:
        return True # Trigger external vector search
    elif "[Retrieve=No]" in model_completion:
        return False # Skip vector search; answer directly
    return False
```

## Interview tips

- Highlight that Self-RAG reduces inference latency and API cost on simple queries by skipping unnecessary vector retrievals.
- Connect Self-RAG reflection tokens to RLHF / DPO fine-tuning setups.

## Related Concepts

- [[How does Plan-and-Solve prompting decompose complex tasks into explicit execution sub-goals?]] (`#136`): [How does Plan-and-Solve prompting decompose complex tasks into explicit execution sub-goals?](../ai-agents-and-mcp/how-does-plan-and-solve-prompting-decompose-complex-tasks-into-explicit-execution-sub-goals.md)
- [[How to measure model hallucination rate using NLI (Natural Language Inference) entailment models?]] (`#176`): [How to measure model hallucination rate using NLI (Natural Language Inference) entailment models?](../evaluation-and-testing/how-to-measure-model-hallucination-rate-using-nli-natural-language-inference-entailment-models.md)
- [[How to build an automated RAG evaluation harness measuring Context Precision and Recall?]] (`#178`): [How to build an automated RAG evaluation harness measuring Context Precision and Recall?](../evaluation-and-testing/how-to-build-an-automated-rag-evaluation-harness-measuring-context-precision-and-recall.md)

---

[⬅ Back to RAG and Vector Databases](./README.md) · [All topics](../README.md)
