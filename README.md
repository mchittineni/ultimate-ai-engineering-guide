<div align="center">

# 🧠 Ultimate AI Engineering Guide

**11 questions across 10 topics - answered to the depth an interviewer actually expects.**

Role tracks: **AI Engineer** (junior → senior) · **Gen AI Engineer** · **LLM Engineer** · **Agentic AI Engineer** · **Forward Deployed Engineer (FDE)** · **AI Systems Architect** · **Applied AI Engineer** · **LLMOps Engineer** · **AI Platform Engineer**

Every answer gives you a short answer you can say out loud, the detail and trade-offs behind it, a runnable example, and the follow-ups to expect.

[![Validate](https://github.com/mchittineni/ultimate-ai-engineering-guide/actions/workflows/validate-and-format.yml/badge.svg)](https://github.com/mchittineni/ultimate-ai-engineering-guide/actions/workflows/validate-and-format.yml)
![Questions](https://img.shields.io/badge/questions-11-blue)
![Topics](https://img.shields.io/badge/topics-10-blueviolet)
![Difficulty](https://img.shields.io/badge/difficulty-🟢%200%20·%20🟡%2011%20·%20🔴%200-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

[Pick your role](#-pick-your-role) · [Browse topics](#-browse-all-topics) · [All questions](#-all-questions) · [How answers are structured](#-how-answers-are-structured) · [Contributing](./CONTRIBUTING.md)

⭐ Star the project if it helps you land the role.

</div>

---

## 🚀 Pick your role

Seven role tracks, each a structured reading order rather than a random collection of links. Start at the left and work right.

> **Interview in a fortnight?** Start with [Interview Experience](./interview-experience/README.md) - it covers the round structure across AI Engineer vs ML Engineer vs FDE, how to present your portfolio, project deep dives, and scenario checklists cross-linked to every answer in this guide.

| 🎯 Target role                      | Read in this order                                                                                                                                                                                                                                                               |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Interviewing now**                | [Interview Experience](./interview-experience/README.md) → [LLM Fundamentals](./llm-fundamentals/README.md) → [Prompt Engineering](./prompt-engineering/README.md) → [RAG & Vector DBs](./rag-and-vector-databases/README.md) → [AI Agents & MCP](./ai-agents-and-mcp/README.md) |
| **AI Engineer**                     | [LLM Fundamentals](./llm-fundamentals/README.md) → [Prompt Engineering](./prompt-engineering/README.md) → [RAG & Vector DBs](./rag-and-vector-databases/README.md) → [AI Agents & MCP](./ai-agents-and-mcp/README.md) → [AI System Design](./ai-system-design/README.md)         |
| **Gen AI Engineer**                 | [Prompt Engineering](./prompt-engineering/README.md) → [RAG & Vector DBs](./rag-and-vector-databases/README.md) → [Fine-Tuning & Adaptation](./fine-tuning-and-adaptation/README.md) → [Evaluation & Testing](./evaluation-and-testing/README.md)                                |
| **Agentic AI Engineer**             | [Prompt Engineering](./prompt-engineering/README.md) → [AI Agents & MCP](./ai-agents-and-mcp/README.md) → [LLM Fundamentals](./llm-fundamentals/README.md) → [AI Safety & Governance](./ai-safety-and-governance/README.md)                                                      |
| **Forward Deployed Engineer (FDE)** | [Interview Experience](./interview-experience/README.md) → [AI Agents & MCP](./ai-agents-and-mcp/README.md) → [RAG & Vector DBs](./rag-and-vector-databases/README.md) → [AI Safety & Governance](./ai-safety-and-governance/README.md)                                          |
| **LLMOps / Production AI**          | [AI System Design](./ai-system-design/README.md) → [LLMOps & Production AI](./llmops-and-production-ai/README.md) → [Evaluation & Testing](./evaluation-and-testing/README.md) → [AI Safety & Governance](./ai-safety-and-governance/README.md)                                  |
| **AI Systems Architect**            | [AI System Design](./ai-system-design/README.md) → [Fine-Tuning & Adaptation](./fine-tuning-and-adaptation/README.md) → [LLM Fundamentals](./llm-fundamentals/README.md) → [LLMOps & Production AI](./llmops-and-production-ai/README.md)                                        |

---

## 📚 Browse all topics

Grouped by theme, with question counts and difficulty mix. Click a topic to open its index, which opens with what interviewers probe there.

<!-- STATS:START -->

**9 questions** across **10 topics** - 🟢 0 Beginner · 🟡 9 Intermediate · 🔴 0 Advanced

### 🧱 Foundations & Models

| Topic                                                    | Questions | 🟢  | 🟡  | 🔴  | What it covers                                                                                   |
| -------------------------------------------------------- | --------- | --- | --- | --- | ------------------------------------------------------------------------------------------------ |
| **[Llm Fundamentals](./llm-fundamentals/README.md)**     | 0         | 0   | 0   | 0   | Core architectures, Transformer mechanics, self-attention, context windows, tokenization, KV…    |
| **[Prompt Engineering](./prompt-engineering/README.md)** | 1         | 0   | 1   | 0   | Zero/few-shot, Chain-of-Thought (CoT), Tree-of-Thoughts, ReAct, system prompts, structured JSON… |

### 🧠 Retrieval & Agentic Systems

| Topic                                                                | Questions | 🟢  | 🟡  | 🔴  | What it covers                                                                                    |
| -------------------------------------------------------------------- | --------- | --- | --- | --- | ------------------------------------------------------------------------------------------------- |
| **[RAG and Vector Databases](./rag-and-vector-databases/README.md)** | 1         | 0   | 1   | 0   | Embeddings, vector indexing (HNSW, IVFFlat), hybrid search, chunking strategies, re-ranking, and… |
| **[AI Agents and MCP](./ai-agents-and-mcp/README.md)**               | 1         | 0   | 1   | 0   | Agentic workflows, Model Context Protocol (MCP), function calling, tool use, memory persistence,… |

### ⚙️ Adaptation & System Design

| Topic                                                                    | Questions | 🟢  | 🟡  | 🔴  | What it covers                                                                                   |
| ------------------------------------------------------------------------ | --------- | --- | --- | --- | ------------------------------------------------------------------------------------------------ |
| **[Fine-Tuning and Adaptation](./fine-tuning-and-adaptation/README.md)** | 1         | 0   | 1   | 0   | PEFT, LoRA, QLoRA, RLHF, DPO, GRPO, quantization (GGUF, AWQ, GPTQ), model distillation, and…     |
| **[AI System Design](./ai-system-design/README.md)**                     | 1         | 0   | 1   | 0   | High-throughput inference, TTFT/TPOT, streaming (SSE), semantic caching, GPU resource planning,… |

### 📊 Operations & Quality

| Topic                                                                | Questions | 🟢  | 🟡  | 🔴  | What it covers                                                                                  |
| -------------------------------------------------------------------- | --------- | --- | --- | --- | ----------------------------------------------------------------------------------------------- |
| **[LLMOps and Production AI](./llmops-and-production-ai/README.md)** | 1         | 0   | 1   | 0   | Observability, prompt tracing, cost management, drift detection, CI/CD pipelines for prompts &… |
| **[Evaluation and Testing](./evaluation-and-testing/README.md)**     | 1         | 0   | 1   | 0   | LLM-as-a-Judge, Ragas metrics (Faithfulness, Relevance), benchmarks (MMLU, HumanEval), unit…    |

### 🛡️ Governance & Career Track

| Topic                                                                | Questions | 🟢  | 🟡  | 🔴  | What it covers                                                                            |
| -------------------------------------------------------------------- | --------- | --- | --- | --- | ----------------------------------------------------------------------------------------- |
| **[AI Safety and Governance](./ai-safety-and-governance/README.md)** | 1         | 0   | 1   | 0   | Data privacy, PII masking, guardrails (NeMo, Llama Guard), alignment tax, copyright, and… |
| **[Interview Experience](./interview-experience/README.md)**         | 1         | 0   | 1   | 0   | Role-specific interview blueprints (AI Engineer, FDE, AI Architect), portfolio project…   |

<!-- STATS:END -->

---

## 📖 All questions

Click any topic to expand its questions, sorted by difficulty level.

<!-- TOC:START -->

### 🧱 Foundations & Models

_1 questions_

<details>
<summary><b>Llm Fundamentals</b> · 0 questions · 🟢 0 🟡 0 🔴 0</summary>

[Open the Llm Fundamentals index →](./llm-fundamentals/README.md)

| No. | Question                                    | Difficulty |
| --- | ------------------------------------------- | ---------- |
| -   | _No questions yet - contributions welcome._ | -          |

</details>

<details>
<summary><b>Prompt Engineering</b> · 1 questions · 🟢 0 🟡 1 🔴 0</summary>

[Open the Prompt Engineering index →](./prompt-engineering/README.md)

| No. | Question                                                                                                                            | Difficulty      |
| --- | ----------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 3   | [How does ReAct (Reasoning and Acting) prompting work?](./prompt-engineering/how-does-react-reasoning-and-acting-prompting-work.md) | 🟡 Intermediate |

</details>

### 🧠 Retrieval & Agentic Systems

_2 questions_

<details>
<summary><b>RAG and Vector Databases</b> · 1 questions · 🟢 0 🟡 1 🔴 0</summary>

[Open the RAG and Vector Databases index →](./rag-and-vector-databases/README.md)

| No. | Question                                                                                                                                                        | Difficulty      |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 4   | [What is the difference between HNSW and IVFFlat vector indexes?](./rag-and-vector-databases/what-is-the-difference-between-hnsw-and-ivfflat-vector-indexes.md) | 🟡 Intermediate |

</details>

<details>
<summary><b>AI Agents and MCP</b> · 1 questions · 🟢 0 🟡 1 🔴 0</summary>

[Open the AI Agents and MCP index →](./ai-agents-and-mcp/README.md)

| No. | Question                                                                                                                                             | Difficulty      |
| --- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 5   | [What is the Model Context Protocol (MCP) and how does it work?](./ai-agents-and-mcp/what-is-the-model-context-protocol-mcp-and-how-does-it-work.md) | 🟡 Intermediate |

</details>

### ⚙️ Adaptation & System Design

_2 questions_

<details>
<summary><b>Fine-Tuning and Adaptation</b> · 1 questions · 🟢 0 🟡 1 🔴 0</summary>

[Open the Fine-Tuning and Adaptation index →](./fine-tuning-and-adaptation/README.md)

| No. | Question                                                                                                                              | Difficulty      |
| --- | ------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 6   | [What is LoRA and QLoRA for efficient fine-tuning?](./fine-tuning-and-adaptation/what-is-lora-and-qlora-for-efficient-fine-tuning.md) | 🟡 Intermediate |

</details>

<details>
<summary><b>AI System Design</b> · 1 questions · 🟢 0 🟡 1 🔴 0</summary>

[Open the AI System Design index →](./ai-system-design/README.md)

| No. | Question                                                                                                                                                                            | Difficulty      |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 7   | [How do you optimize Time to First Token (TTFT) vs Time Per Output Token (TPOT)?](./ai-system-design/how-do-you-optimize-time-to-first-token-ttft-vs-time-per-output-token-tpot.md) | 🟡 Intermediate |

</details>

### 📊 Operations & Quality

_2 questions_

<details>
<summary><b>LLMOps and Production AI</b> · 1 questions · 🟢 0 🟡 1 🔴 0</summary>

[Open the LLMOps and Production AI index →](./llmops-and-production-ai/README.md)

| No. | Question                                                                                                                                                                      | Difficulty      |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 8   | [How do you implement distributed tracing for multi-step LLM pipelines?](./llmops-and-production-ai/how-do-you-implement-distributed-tracing-for-multi-step-llm-pipelines.md) | 🟡 Intermediate |

</details>

<details>
<summary><b>Evaluation and Testing</b> · 1 questions · 🟢 0 🟡 1 🔴 0</summary>

[Open the Evaluation and Testing index →](./evaluation-and-testing/README.md)

| No. | Question                                                                                                                                                                          | Difficulty      |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 9   | [How do Faithfulness, Context Recall, and Answer Relevance differ in Ragas?](./evaluation-and-testing/how-do-faithfulness-context-recall-and-answer-relevance-differ-in-ragas.md) | 🟡 Intermediate |

</details>

### 🛡️ Governance & Career Track

_2 questions_

<details>
<summary><b>AI Safety and Governance</b> · 1 questions · 🟢 0 🟡 1 🔴 0</summary>

[Open the AI Safety and Governance index →](./ai-safety-and-governance/README.md)

| No. | Question                                                                                                                                                                    | Difficulty      |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 10  | [How do input and output guardrails prevent jailbreaks and data leaks?](./ai-safety-and-governance/how-do-input-and-output-guardrails-prevent-jailbreaks-and-data-leaks.md) | 🟡 Intermediate |

</details>

<details>
<summary><b>Interview Experience</b> · 1 questions · 🟢 0 🟡 1 🔴 0</summary>

[Open the Interview Experience index →](./interview-experience/README.md)

| No. | Question                                                                                                                                                                              | Difficulty      |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 11  | [What are the key differences between AI Engineer, ML Engineer, and FDE roles?](./interview-experience/what-are-the-key-differences-between-ai-engineer-ml-engineer-and-fde-roles.md) | 🟡 Intermediate |

</details>

<!-- TOC:END -->

---

## 📝 How answers are structured

Every question in this repository adheres to a strict four-part structure:

1. **Short answer:** A 1-2 sentence core answer you can say out loud in an interview.
2. **Detail:** Deep-dive technical explanation covering internal mechanics, equations, architecture flows, and production trade-offs.
3. **Example:** Concrete Python/PyTorch code snippet, prompt template, config file, or comparative table.
4. **Interview tips:** What interviewers probe next, common traps, and real-world failure modes.

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on adding new questions, running local validation tools, and maintaining index freshness.

```bash
# Validate frontmatter, links, IDs, and structure
python3 scripts/validate_content.py

# Regenerate topic indexes and README stats
python3 scripts/generate_indexes.py
```text

---

## 📄 License

This repository is licensed under the [MIT License](./LICENSE).
