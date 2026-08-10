<div align="center">

# 🧠 Ultimate AI Engineering Guide

**100 questions across 10 topics - answered to the depth an interviewer actually expects.**

Role tracks: **AI Engineer** (junior → senior) · **Gen AI Engineer** · **LLM Engineer** · **Agentic AI Engineer** · **Forward Deployed Engineer (FDE)** · **AI Systems Architect** · **Applied AI Engineer** · **LLMOps Engineer** · **AI Platform Engineer**

Every answer gives you a short answer you can say out loud, the detail and trade-offs behind it, a runnable example, and the follow-ups to expect.

[![Validate](https://github.com/mchittineni/ultimate-ai-engineering-guide/actions/workflows/validate-and-format.yml/badge.svg)](https://github.com/mchittineni/ultimate-ai-engineering-guide/actions/workflows/validate-and-format.yml)
![Questions](https://img.shields.io/badge/questions-100-blue)
![Topics](https://img.shields.io/badge/topics-10-blueviolet)
![Difficulty](https://img.shields.io/badge/difficulty-🟢%2050%20·%20🟡%2030%20·%20🔴%2020-lightgrey)
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

**100 questions** across **10 topics** - 🟢 50 Beginner · 🟡 30 Intermediate · 🔴 20 Advanced

### 🧱 Foundations & Models

| Topic                                                    | Questions | 🟢  | 🟡  | 🔴  | What it covers                                                                                   |
| -------------------------------------------------------- | --------- | --- | --- | --- | ------------------------------------------------------------------------------------------------ |
| **[LLM Fundamentals](./llm-fundamentals/README.md)**     | 10        | 5   | 3   | 2   | Core architectures, Transformer mechanics, self-attention, context windows, tokenization, KV…    |
| **[Prompt Engineering](./prompt-engineering/README.md)** | 10        | 5   | 3   | 2   | Zero/few-shot, Chain-of-Thought (CoT), Tree-of-Thoughts, ReAct, system prompts, structured JSON… |

### 🧠 Retrieval & Agentic Systems

| Topic                                                                | Questions | 🟢  | 🟡  | 🔴  | What it covers                                                                                    |
| -------------------------------------------------------------------- | --------- | --- | --- | --- | ------------------------------------------------------------------------------------------------- |
| **[RAG and Vector Databases](./rag-and-vector-databases/README.md)** | 10        | 5   | 3   | 2   | Embeddings, vector indexing (HNSW, IVFFlat), hybrid search, chunking strategies, re-ranking, and… |
| **[AI Agents and MCP](./ai-agents-and-mcp/README.md)**               | 10        | 5   | 3   | 2   | Agentic workflows, Model Context Protocol (MCP), function calling, tool use, memory persistence,… |

### ⚙️ Adaptation & System Design

| Topic                                                                    | Questions | 🟢  | 🟡  | 🔴  | What it covers                                                                                   |
| ------------------------------------------------------------------------ | --------- | --- | --- | --- | ------------------------------------------------------------------------------------------------ |
| **[Fine-Tuning and Adaptation](./fine-tuning-and-adaptation/README.md)** | 10        | 5   | 3   | 2   | PEFT, LoRA, QLoRA, RLHF, DPO, GRPO, quantization (GGUF, AWQ, GPTQ), model distillation, and…     |
| **[AI System Design](./ai-system-design/README.md)**                     | 10        | 5   | 3   | 2   | High-throughput inference, TTFT/TPOT, streaming (SSE), semantic caching, GPU resource planning,… |

### 📊 Operations & Quality

| Topic                                                                | Questions | 🟢  | 🟡  | 🔴  | What it covers                                                                                  |
| -------------------------------------------------------------------- | --------- | --- | --- | --- | ----------------------------------------------------------------------------------------------- |
| **[LLMOps and Production AI](./llmops-and-production-ai/README.md)** | 10        | 5   | 3   | 2   | Observability, prompt tracing, cost management, drift detection, CI/CD pipelines for prompts &… |
| **[Evaluation and Testing](./evaluation-and-testing/README.md)**     | 10        | 5   | 3   | 2   | LLM-as-a-Judge, Ragas metrics (Faithfulness, Relevance), benchmarks (MMLU, HumanEval), unit…    |

### 🛡️ Governance & Career Track

| Topic                                                                | Questions | 🟢  | 🟡  | 🔴  | What it covers                                                                            |
| -------------------------------------------------------------------- | --------- | --- | --- | --- | ----------------------------------------------------------------------------------------- |
| **[AI Safety and Governance](./ai-safety-and-governance/README.md)** | 10        | 5   | 3   | 2   | Data privacy, PII masking, guardrails (NeMo, Llama Guard), alignment tax, copyright, and… |
| **[Interview Experience](./interview-experience/README.md)**         | 10        | 5   | 3   | 2   | Role-specific interview blueprints (AI Engineer, FDE, AI Architect), portfolio project…   |

<!-- STATS:END -->

---

## 📖 All questions

Click any topic to expand its questions, sorted by difficulty level.

<!-- TOC:START -->

### 🧱 Foundations & Models

_20 questions_

<details>
<summary><b>LLM Fundamentals</b> · 10 questions · 🟢 5 🟡 3 🔴 2</summary>

[Open the LLM Fundamentals index →](./llm-fundamentals/README.md)

| No. | Question                                                                                                                                                                                        | Difficulty      |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 1   | [What is KV Cache and how does it speed up inference?](./llm-fundamentals/what-is-kv-cache-and-how-does-it-speed-up-inference.md)                                                               | 🟡 Intermediate |
| 2   | [How does Grouped-Query Attention (GQA) differ from Multi-Head Attention (MHA)?](./llm-fundamentals/how-does-grouped-query-attention-gqa-differ-from-multi-head-attention-mha.md)               | 🟡 Intermediate |
| 12  | [What is the difference between encoder-only, decoder-only, and encoder-decoder LLMs?](./llm-fundamentals/what-is-the-difference-between-encoder-only-decoder-only-and-encoder-decoder-llms.md) | 🟢 Beginner     |
| 13  | [How does Byte-Pair Encoding (BPE) tokenization work?](./llm-fundamentals/how-does-byte-pair-encoding-bpe-tokenization-work.md)                                                                 | 🟢 Beginner     |
| 14  | [How do Rotary Position Embeddings (RoPE) and RoPE scaling work?](./llm-fundamentals/how-do-rotary-position-embeddings-rope-and-rope-scaling-work.md)                                           | 🔴 Advanced     |
| 51  | [What is Temperature, Top-p, and Top-k sampling?](./llm-fundamentals/what-is-temperature-top-p-and-top-k-sampling.md)                                                                           | 🟢 Beginner     |
| 52  | [What is the difference between greedy decoding and beam search?](./llm-fundamentals/what-is-the-difference-between-greedy-decoding-and-beam-search.md)                                         | 🟢 Beginner     |
| 53  | [What is a context window and how does it limit LLM processing?](./llm-fundamentals/what-is-a-context-window-and-how-does-it-limit-llm-processing.md)                                           | 🟢 Beginner     |
| 54  | [How does Multi-Query Attention (MQA) differ from Multi-Head Attention?](./llm-fundamentals/how-does-multi-query-attention-mqa-differ-from-multi-head-attention.md)                             | 🟡 Intermediate |
| 55  | [How does FlashAttention optimize memory and speed via tiling?](./llm-fundamentals/how-does-flashattention-optimize-memory-and-speed-via-tiling.md)                                             | 🔴 Advanced     |

</details>

<details>
<summary><b>Prompt Engineering</b> · 10 questions · 🟢 5 🟡 3 🔴 2</summary>

[Open the Prompt Engineering index →](./prompt-engineering/README.md)

| No. | Question                                                                                                                                                                            | Difficulty      |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 3   | [How does ReAct (Reasoning and Acting) prompting work?](./prompt-engineering/how-does-react-reasoning-and-acting-prompting-work.md)                                                 | 🟡 Intermediate |
| 15  | [What is the difference between zero-shot and few-shot prompting?](./prompt-engineering/what-is-the-difference-between-zero-shot-and-few-shot-prompting.md)                         | 🟢 Beginner     |
| 16  | [How does Chain-of-Thought (CoT) prompting improve LLM reasoning?](./prompt-engineering/how-does-chain-of-thought-cot-prompting-improve-llm-reasoning.md)                           | 🟢 Beginner     |
| 17  | [How do you enforce structured JSON outputs from an LLM?](./prompt-engineering/how-do-you-enforce-structured-json-outputs-from-an-llm.md)                                           | 🟡 Intermediate |
| 18  | [How does Tree-of-Thoughts (ToT) prompting differ from Chain-of-Thought?](./prompt-engineering/how-does-tree-of-thoughts-tot-prompting-differ-from-chain-of-thought.md)             | 🔴 Advanced     |
| 56  | [What is a system prompt and how does it steer model behavior?](./prompt-engineering/what-is-a-system-prompt-and-how-does-it-steer-model-behavior.md)                               | 🟢 Beginner     |
| 57  | [What is prompt leaking and how do you prevent it?](./prompt-engineering/what-is-prompt-leaking-and-how-do-you-prevent-it.md)                                                       | 🟢 Beginner     |
| 58  | [How do role prompting and persona framing affect LLM outputs?](./prompt-engineering/how-do-role-prompting-and-persona-framing-affect-llm-outputs.md)                               | 🟢 Beginner     |
| 59  | [How do you design few-shot examples to prevent label bias?](./prompt-engineering/how-do-you-design-few-shot-examples-to-prevent-label-bias.md)                                     | 🟡 Intermediate |
| 60  | [How does Skeleton-of-Thought (SoT) speed up generation via parallel decoding?](./prompt-engineering/how-does-skeleton-of-thought-sot-speed-up-generation-via-parallel-decoding.md) | 🔴 Advanced     |

</details>

### 🧠 Retrieval & Agentic Systems

_20 questions_

<details>
<summary><b>RAG and Vector Databases</b> · 10 questions · 🟢 5 🟡 3 🔴 2</summary>

[Open the RAG and Vector Databases index →](./rag-and-vector-databases/README.md)

| No. | Question                                                                                                                                                                            | Difficulty      |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 4   | [What is the difference between HNSW and IVFFlat vector indexes?](./rag-and-vector-databases/what-is-the-difference-between-hnsw-and-ivfflat-vector-indexes.md)                     | 🟡 Intermediate |
| 19  | [What is Retrieval-Augmented Generation (RAG) and why is it used?](./rag-and-vector-databases/what-is-retrieval-augmented-generation-rag-and-why-is-it-used.md)                     | 🟢 Beginner     |
| 20  | [How do dense and sparse vector embeddings differ?](./rag-and-vector-databases/how-do-dense-and-sparse-vector-embeddings-differ.md)                                                 | 🟢 Beginner     |
| 21  | [How does hybrid search combine BM25 and vector embeddings?](./rag-and-vector-databases/how-does-hybrid-search-combine-bm25-and-vector-embeddings.md)                               | 🟡 Intermediate |
| 22  | [How do cross-encoder rerankers and late-interaction (ColBERT) models work?](./rag-and-vector-databases/how-do-cross-encoder-rerankers-and-late-interaction-colbert-models-work.md) | 🔴 Advanced     |
| 61  | [What is chunk size and chunk overlap in text splitting?](./rag-and-vector-databases/what-is-chunk-size-and-chunk-overlap-in-text-splitting.md)                                     | 🟢 Beginner     |
| 62  | [What is Cosine Similarity vs Euclidean Distance in vector search?](./rag-and-vector-databases/what-is-cosine-similarity-vs-euclidean-distance-in-vector-search.md)                 | 🟢 Beginner     |
| 63  | [What is the 'Lost in the Middle' phenomenon in LLM retrieval?](./rag-and-vector-databases/what-is-the-lost-in-the-middle-phenomenon-in-llm-retrieval.md)                           | 🟢 Beginner     |
| 64  | [How does query rewriting and Hypothetical Document Embeddings (HyDE) work?](./rag-and-vector-databases/how-does-query-rewriting-and-hypothetical-document-embeddings-hyde-work.md) | 🟡 Intermediate |
| 65  | [How do GraphRAG and Knowledge Graphs enhance vector retrieval?](./rag-and-vector-databases/how-do-graphrag-and-knowledge-graphs-enhance-vector-retrieval.md)                       | 🔴 Advanced     |

</details>

<details>
<summary><b>AI Agents and MCP</b> · 10 questions · 🟢 5 🟡 3 🔴 2</summary>

[Open the AI Agents and MCP index →](./ai-agents-and-mcp/README.md)

| No. | Question                                                                                                                                                                   | Difficulty      |
| --- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 5   | [What is the Model Context Protocol (MCP) and how does it work?](./ai-agents-and-mcp/what-is-the-model-context-protocol-mcp-and-how-does-it-work.md)                       | 🟡 Intermediate |
| 23  | [What is an AI agent and how does it differ from a standard LLM?](./ai-agents-and-mcp/what-is-an-ai-agent-and-how-does-it-differ-from-a-standard-llm.md)                   | 🟢 Beginner     |
| 24  | [How does LLM tool use and function calling work?](./ai-agents-and-mcp/how-does-llm-tool-use-and-function-calling-work.md)                                                 | 🟢 Beginner     |
| 25  | [How do you manage short-term and long-term memory in AI agents?](./ai-agents-and-mcp/how-do-you-manage-short-term-and-long-term-memory-in-ai-agents.md)                   | 🟡 Intermediate |
| 26  | [How do multi-agent architectures and hierarchical delegation work?](./ai-agents-and-mcp/how-do-multi-agent-architectures-and-hierarchical-delegation-work.md)             | 🔴 Advanced     |
| 66  | [What is the ReAct loop (Thought, Action, Observation)?](./ai-agents-and-mcp/what-is-the-react-loop-thought-action-observation.md)                                         | 🟢 Beginner     |
| 67  | [What is an MCP Tool vs an MCP Resource in Model Context Protocol?](./ai-agents-and-mcp/what-is-an-mcp-tool-vs-an-mcp-resource-in-model-context-protocol.md)               | 🟢 Beginner     |
| 68  | [How do you handle tool execution errors in agentic loops?](./ai-agents-and-mcp/how-do-you-handle-tool-execution-errors-in-agentic-loops.md)                               | 🟢 Beginner     |
| 69  | [How does MCP server-client architecture standardize context connections?](./ai-agents-and-mcp/how-does-mcp-server-client-architecture-standardize-context-connections.md) | 🟡 Intermediate |
| 70  | [How do you prevent infinite agentic loops and runaway execution?](./ai-agents-and-mcp/how-do-you-prevent-infinite-agentic-loops-and-runaway-execution.md)                 | 🔴 Advanced     |

</details>

### ⚙️ Adaptation & System Design

_20 questions_

<details>
<summary><b>Fine-Tuning and Adaptation</b> · 10 questions · 🟢 5 🟡 3 🔴 2</summary>

[Open the Fine-Tuning and Adaptation index →](./fine-tuning-and-adaptation/README.md)

| No. | Question                                                                                                                                                                                              | Difficulty      |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 6   | [What is LoRA and QLoRA for efficient fine-tuning?](./fine-tuning-and-adaptation/what-is-lora-and-qlora-for-efficient-fine-tuning.md)                                                                 | 🟡 Intermediate |
| 27  | [What is the difference between pre-training, fine-tuning, and in-context learning?](./fine-tuning-and-adaptation/what-is-the-difference-between-pre-training-fine-tuning-and-in-context-learning.md) | 🟢 Beginner     |
| 28  | [What is quantization and how do INT8 and INT4 reduce LLM footprint?](./fine-tuning-and-adaptation/what-is-quantization-and-how-do-int8-and-int4-reduce-llm-footprint.md)                             | 🟢 Beginner     |
| 29  | [How does Direct Preference Optimization (DPO) differ from RLHF?](./fine-tuning-and-adaptation/how-does-direct-preference-optimization-dpo-differ-from-rlhf.md)                                       | 🟡 Intermediate |
| 30  | [How does Group Relative Policy Optimization (GRPO) work in DeepSeek R1?](./fine-tuning-and-adaptation/how-does-group-relative-policy-optimization-grpo-work-in-deepseek-r1.md)                       | 🔴 Advanced     |
| 71  | [What is Supervised Fine-Tuning (SFT) and when is it required?](./fine-tuning-and-adaptation/what-is-supervised-fine-tuning-sft-and-when-is-it-required.md)                                           | 🟢 Beginner     |
| 72  | [What is catastrophic forgetting during LLM fine-tuning?](./fine-tuning-and-adaptation/what-is-catastrophic-forgetting-during-llm-fine-tuning.md)                                                     | 🟢 Beginner     |
| 73  | [What is LoRA rank r and alpha scaling factor?](./fine-tuning-and-adaptation/what-is-lora-rank-r-and-alpha-scaling-factor.md)                                                                         | 🟢 Beginner     |
| 74  | [How does model distillation transfer knowledge from teacher to student?](./fine-tuning-and-adaptation/how-does-model-distillation-transfer-knowledge-from-teacher-to-student.md)                     | 🟡 Intermediate |
| 75  | [How does Kahneman-Tversky Optimization (KTO) differ from DPO?](./fine-tuning-and-adaptation/how-does-kahneman-tversky-optimization-kto-differ-from-dpo.md)                                           | 🔴 Advanced     |

</details>

<details>
<summary><b>AI System Design</b> · 10 questions · 🟢 5 🟡 3 🔴 2</summary>

[Open the AI System Design index →](./ai-system-design/README.md)

| No. | Question                                                                                                                                                                            | Difficulty      |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 7   | [How do you optimize Time to First Token (TTFT) vs Time Per Output Token (TPOT)?](./ai-system-design/how-do-you-optimize-time-to-first-token-ttft-vs-time-per-output-token-tpot.md) | 🟡 Intermediate |
| 31  | [What is Server-Sent Events (SSE) streaming for LLM responses?](./ai-system-design/what-is-server-sent-events-sse-streaming-for-llm-responses.md)                                   | 🟢 Beginner     |
| 32  | [How does semantic caching reduce LLM API latency and cost?](./ai-system-design/how-does-semantic-caching-reduce-llm-api-latency-and-cost.md)                                       | 🟢 Beginner     |
| 33  | [How does PagedAttention in vLLM solve memory fragmentation?](./ai-system-design/how-does-pagedattention-in-vllm-solve-memory-fragmentation.md)                                     | 🟡 Intermediate |
| 34  | [How does speculative decoding speed up LLM inference?](./ai-system-design/how-does-speculative-decoding-speed-up-llm-inference.md)                                                 | 🔴 Advanced     |
| 76  | [What is continuous batching and how does it improve GPU utilization?](./ai-system-design/what-is-continuous-batching-and-how-does-it-improve-gpu-utilization.md)                   | 🟢 Beginner     |
| 77  | [What is the difference between prefill phase and decoding phase?](./ai-system-design/what-is-the-difference-between-prefill-phase-and-decoding-phase.md)                           | 🟢 Beginner     |
| 78  | [What is GPU VRAM bandwidth and why is decoding memory-bound?](./ai-system-design/what-is-gpu-vram-bandwidth-and-why-is-decoding-memory-bound.md)                                   | 🟢 Beginner     |
| 79  | [How do you design a multi-tenant LLM gateway with rate limits?](./ai-system-design/how-do-you-design-a-multi-tenant-llm-gateway-with-rate-limits.md)                               | 🟡 Intermediate |
| 80  | [How does chunked prefill disaggregate prefill and decoding nodes?](./ai-system-design/how-does-chunked-prefill-disaggregate-prefill-and-decoding-nodes.md)                         | 🔴 Advanced     |

</details>

### 📊 Operations & Quality

_20 questions_

<details>
<summary><b>LLMOps and Production AI</b> · 10 questions · 🟢 5 🟡 3 🔴 2</summary>

[Open the LLMOps and Production AI index →](./llmops-and-production-ai/README.md)

| No. | Question                                                                                                                                                                            | Difficulty      |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 8   | [How do you implement distributed tracing for multi-step LLM pipelines?](./llmops-and-production-ai/how-do-you-implement-distributed-tracing-for-multi-step-llm-pipelines.md)       | 🟡 Intermediate |
| 35  | [What is LLMOps and how does it differ from traditional MLOps?](./llmops-and-production-ai/what-is-llmops-and-how-does-it-differ-from-traditional-mlops.md)                         | 🟢 Beginner     |
| 36  | [How do you monitor LLM token usage, latency, and costs in production?](./llmops-and-production-ai/how-do-you-monitor-llm-token-usage-latency-and-costs-in-production.md)           | 🟢 Beginner     |
| 37  | [How do you implement fallback routing and rate limiting for LLM APIs?](./llmops-and-production-ai/how-do-you-implement-fallback-routing-and-rate-limiting-for-llm-apis.md)         | 🟡 Intermediate |
| 38  | [How do you detect and mitigate data and concept drift in production LLMs?](./llmops-and-production-ai/how-do-you-detect-and-mitigate-data-and-concept-drift-in-production-llms.md) | 🔴 Advanced     |
| 81  | [What is prompt versioning and why is it essential?](./llmops-and-production-ai/what-is-prompt-versioning-and-why-is-it-essential.md)                                               | 🟢 Beginner     |
| 82  | [What is an OpenTelemetry span in LLM tracing?](./llmops-and-production-ai/what-is-an-opentelemetry-span-in-llm-tracing.md)                                                         | 🟢 Beginner     |
| 83  | [How do you budget and cap monthly LLM API costs?](./llmops-and-production-ai/how-do-you-budget-and-cap-monthly-llm-api-costs.md)                                                   | 🟢 Beginner     |
| 84  | [How do you build a canary deployment pipeline for prompt updates?](./llmops-and-production-ai/how-do-you-build-a-canary-deployment-pipeline-for-prompt-updates.md)                 | 🟡 Intermediate |
| 85  | [How do you architect real-time anomaly detection for rogue agent spends?](./llmops-and-production-ai/how-do-you-architect-real-time-anomaly-detection-for-rogue-agent-spends.md)   | 🔴 Advanced     |

</details>

<details>
<summary><b>Evaluation and Testing</b> · 10 questions · 🟢 5 🟡 3 🔴 2</summary>

[Open the Evaluation and Testing index →](./evaluation-and-testing/README.md)

| No. | Question                                                                                                                                                                                | Difficulty      |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 9   | [How do Faithfulness, Context Recall, and Answer Relevance differ in Ragas?](./evaluation-and-testing/how-do-faithfulness-context-recall-and-answer-relevance-differ-in-ragas.md)       | 🟡 Intermediate |
| 39  | [What is LLM-as-a-Judge and how is it used for automated evaluations?](./evaluation-and-testing/what-is-llm-as-a-judge-and-how-is-it-used-for-automated-evaluations.md)                 | 🟢 Beginner     |
| 40  | [What are standard LLM benchmarks like MMLU, GSM8K, and HumanEval?](./evaluation-and-testing/what-are-standard-llm-benchmarks-like-mmlu-gsm8k-and-humaneval.md)                         | 🟢 Beginner     |
| 41  | [How do you build a CI/CD prompt regression testing suite?](./evaluation-and-testing/how-do-you-build-a-ci-cd-prompt-regression-testing-suite.md)                                       | 🟡 Intermediate |
| 42  | [How do you mitigate positional bias and self-preference in LLM-as-a-Judge?](./evaluation-and-testing/how-do-you-mitigate-positional-bias-and-self-preference-in-llm-as-a-judge.md)     | 🔴 Advanced     |
| 86  | [What is context precision vs context recall in RAG?](./evaluation-and-testing/what-is-context-precision-vs-context-recall-in-rag.md)                                                   | 🟢 Beginner     |
| 87  | [What is faithfulness vs answer relevance in LLM evals?](./evaluation-and-testing/what-is-faithfulness-vs-answer-relevance-in-llm-evals.md)                                             | 🟢 Beginner     |
| 88  | [What is ground-truth reference data in evaluation harnesses?](./evaluation-and-testing/what-is-ground-truth-reference-data-in-evaluation-harnesses.md)                                 | 🟢 Beginner     |
| 89  | [How do you measure inter-annotator agreement (Cohen's Kappa) with LLM judges?](./evaluation-and-testing/how-do-you-measure-inter-annotator-agreement-cohen-s-kappa-with-llm-judges.md) | 🟡 Intermediate |
| 90  | [How do you build an automated red teaming harness against jailbreaks?](./evaluation-and-testing/how-do-you-build-an-automated-red-teaming-harness-against-jailbreaks.md)               | 🔴 Advanced     |

</details>

### 🛡️ Governance & Career Track

_20 questions_

<details>
<summary><b>AI Safety and Governance</b> · 10 questions · 🟢 5 🟡 3 🔴 2</summary>

[Open the AI Safety and Governance index →](./ai-safety-and-governance/README.md)

| No. | Question                                                                                                                                                                                                              | Difficulty      |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 10  | [How do input and output guardrails prevent jailbreaks and data leaks?](./ai-safety-and-governance/how-do-input-and-output-guardrails-prevent-jailbreaks-and-data-leaks.md)                                           | 🟡 Intermediate |
| 43  | [What is prompt injection and how does it differ from SQL injection?](./ai-safety-and-governance/what-is-prompt-injection-and-how-does-it-differ-from-sql-injection.md)                                               | 🟢 Beginner     |
| 44  | [How do you redact PII (Personally Identifiable Information) before sending prompts to LLMs?](./ai-safety-and-governance/how-do-you-redact-pii-personally-identifiable-information-before-sending-prompts-to-llms.md) | 🟢 Beginner     |
| 45  | [How does Llama Guard classify unsafe inputs and outputs?](./ai-safety-and-governance/how-does-llama-guard-classify-unsafe-inputs-and-outputs.md)                                                                     | 🟡 Intermediate |
| 46  | [What is the alignment tax and how does it impact model reasoning?](./ai-safety-and-governance/what-is-the-alignment-tax-and-how-does-it-impact-model-reasoning.md)                                                   | 🔴 Advanced     |
| 91  | [What is system prompt exfiltration and how to prevent it?](./ai-safety-and-governance/what-is-system-prompt-exfiltration-and-how-to-prevent-it.md)                                                                   | 🟢 Beginner     |
| 92  | [What is data exfiltration via LLM tool calls?](./ai-safety-and-governance/what-is-data-exfiltration-via-llm-tool-calls.md)                                                                                           | 🟢 Beginner     |
| 93  | [What is hallucination and what are its primary causes?](./ai-safety-and-governance/what-is-hallucination-and-what-are-its-primary-causes.md)                                                                         | 🟢 Beginner     |
| 94  | [How do NeMo Guardrails enforce programmable rails using Colang?](./ai-safety-and-governance/how-do-nemo-guardrails-enforce-programmable-rails-using-colang.md)                                                       | 🟡 Intermediate |
| 95  | [How do you enforce strict RBAC and data isolation in enterprise RAG?](./ai-safety-and-governance/how-do-you-enforce-strict-rbac-and-data-isolation-in-enterprise-rag.md)                                             | 🔴 Advanced     |

</details>

<details>
<summary><b>Interview Experience</b> · 10 questions · 🟢 5 🟡 3 🔴 2</summary>

[Open the Interview Experience index →](./interview-experience/README.md)

| No. | Question                                                                                                                                                                                                        | Difficulty      |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 11  | [What are the key differences between AI Engineer, ML Engineer, and FDE roles?](./interview-experience/what-are-the-key-differences-between-ai-engineer-ml-engineer-and-fde-roles.md)                           | 🟡 Intermediate |
| 47  | [How do you prepare for an AI engineering coding interview?](./interview-experience/how-do-you-prepare-for-an-ai-engineering-coding-interview.md)                                                               | 🟢 Beginner     |
| 48  | [How should you present an AI portfolio project to hiring managers?](./interview-experience/how-should-you-present-an-ai-portfolio-project-to-hiring-managers.md)                                               | 🟢 Beginner     |
| 49  | [How do you structure a system design interview response for an LLM application?](./interview-experience/how-do-you-structure-a-system-design-interview-response-for-an-llm-application.md)                     | 🟡 Intermediate |
| 50  | [How do you handle scenario-based trade-off questions in senior AI engineering interviews?](./interview-experience/how-do-you-handle-scenario-based-trade-off-questions-in-senior-ai-engineering-interviews.md) | 🔴 Advanced     |
| 96  | [What are the most common pitfalls in AI engineering coding interviews?](./interview-experience/what-are-the-most-common-pitfalls-in-ai-engineering-coding-interviews.md)                                       | 🟢 Beginner     |
| 97  | [How do you explain LLM hallucination mitigation to interviewers?](./interview-experience/how-do-you-explain-llm-hallucination-mitigation-to-interviewers.md)                                                   | 🟢 Beginner     |
| 98  | [How do you demonstrate production readiness in a take-home AI project?](./interview-experience/how-do-you-demonstrate-production-readiness-in-a-take-home-ai-project.md)                                       | 🟢 Beginner     |
| 99  | [How do you answer 'What is your favorite paper or technique in AI'?](./interview-experience/how-do-you-answer-what-is-your-favorite-paper-or-technique-in-ai.md)                                               | 🟡 Intermediate |
| 100 | [How do you lead an AI system architecture deep dive under ambiguity?](./interview-experience/how-do-you-lead-an-ai-system-architecture-deep-dive-under-ambiguity.md)                                           | 🔴 Advanced     |

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
```

---

## 📄 License

This repository is licensed under the [MIT License](./LICENSE).
