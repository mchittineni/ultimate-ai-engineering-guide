---
title: "What are the core differences between AI Engineer, ML Engineer, and FDE roles?"
id: 193
category: "Interview Experience"
difficulty: "Beginner"
tags:
  - ai-engineering
  - interview-experience
  - interview-questions
---

# What are the core differences between AI Engineer, ML Engineer, and FDE roles?

**Short answer:** AI Engineers focus on building applications, RAG pipelines, agents, and systems around foundation models; ML Engineers focus on model architecture, pre-training, fine-tuning algorithms, and PyTorch CUDA kernels; Forward Deployed Engineers (FDEs) combine AI engineering with customer-facing enterprise system integration.

## Detail

Organizations delineate AI roles based on where focus lies in the technology stack:

```
[ML Engineer / Scientist] ──► Pre-training, Loss Functions, PyTorch CUDA Kernels
           │
           ▼
[AI / GenAI Engineer]     ──► RAG, Prompt Pipelines, Agentic Workflows, Evaluation Harnesses, LLMOps
           │
           ▼
[Forward Deployed Engineer] ──► Customer Integrations, On-Premises Enterprise Deployments, Security RBAC
```

### Core Role Comparison Matrix

| Dimension | AI Engineer | ML Engineer (MLE) | Forward Deployed Engineer (FDE) |
| --- | --- | --- | --- |
| **Primary Stack** | Python, TypeScript, Vector DBs, LangChain/MCP, APIs | PyTorch, CUDA, Distributed Training (DeepSpeed, Megatron) | Python, Cloud/K8s, Enterprise APIs, Customer Codebases |
| **Daily Tasks** | Building RAG, tool-calling agents, evals, prompt pipelines | Model pre-training, RLHF alignment, custom layer math | Custom customer integrations, technical deployment, pilot builds |
| **Key Metric** | Application quality, latency SLAs, user metrics | Loss convergence, benchmark accuracy (MMLU), FLOPs efficiency | Customer adoption, pilot conversion, integration speed |

## Example

Self-identification summary to present in interviews:

```markdown
"As an AI Engineer, my core strength lies in translating complex business requirements into production AI applications—optimizing RAG retrieval precision, building resilient agentic tool loops, enforcing strict evaluation harnesses, and governing token latency and API cost."
```

## Interview tips

- Align your portfolio and interview answers with the specific role expectations: emphasize system integration and evaluation for AI Engineer/FDE roles vs math and model training for MLE roles.
- Emphasize cross-functional skills: combining software engineering rigor with AI domain knowledge.

## Related Concepts

- [[How to prepare for an AI Engineer coding interview (raw SDK vs frameworks)?]] (`#191`): [How to prepare for an AI Engineer coding interview (raw SDK vs frameworks)?](../interview-experience/how-to-prepare-for-an-ai-engineer-coding-interview-raw-sdk-vs-frameworks.md)
- [[How to answer scenario questions about trade-offs between RAG and Fine-Tuning?]] (`#194`): [How to answer scenario questions about trade-offs between RAG and Fine-Tuning?](../interview-experience/how-to-answer-scenario-questions-about-trade-offs-between-rag-and-fine-tuning.md)
- [[How to demonstrate production-grade AI engineering rigor over toy notebook demos?]] (`#198`): [How to demonstrate production-grade AI engineering rigor over toy notebook demos?](../interview-experience/how-to-demonstrate-production-grade-ai-engineering-rigor-over-toy-notebook-demos.md)

---

[⬅ Back to Interview Experience](./README.md) · [All topics](../README.md)
