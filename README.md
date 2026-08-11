<div align="center">

# 🧠 Ultimate AI Engineering Guide

**205 questions across 10 topics - answered to the depth an interviewer actually expects.**

Role tracks: **AI Engineer** (junior → senior) · **Gen AI Engineer** · **LLM Engineer** · **Agentic AI Engineer** · **Forward Deployed Engineer (FDE)** · **AI Systems Architect** · **Applied AI Engineer** · **LLMOps Engineer** · **AI Platform Engineer**

Every answer gives you a short answer you can say out loud, the detail and trade-offs behind it, a runnable example, and the follow-ups to expect.

[![Validate](https://github.com/mchittineni/ultimate-ai-engineering-guide/actions/workflows/validate-and-format.yml/badge.svg)](https://github.com/mchittineni/ultimate-ai-engineering-guide/actions/workflows/validate-and-format.yml)
[![Knowledge Graph](https://img.shields.io/badge/interactive-3D%20Knowledge%20Graph-8b5cf6?style=flat&logo=webgl)](https://mchittineni.github.io/ultimate-ai-engineering-guide/)
![Questions](https://img.shields.io/badge/questions-205-blue)
![Topics](https://img.shields.io/badge/topics-10-blueviolet)
![Difficulty](https://img.shields.io/badge/difficulty-🟢%20101%20·%20🟡%2062%20·%20🔴%2042-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

[🌐 3D Knowledge Graph](https://mchittineni.github.io/ultimate-ai-engineering-guide/) · [Pick your role](#-pick-your-role) · [Browse topics](#-browse-all-topics) · [All questions](#-all-questions) · [How answers are structured](#-how-answers-are-structured) · [Contributing](./CONTRIBUTING.md)

⭐ Star the project if it helps you land the role.

</div>

---

## 🌐 Interactive 3D Knowledge Graph

This repository features an interactive **WebGL 3D Force-Directed Knowledge Graph** published via GitHub Pages.

👉 **[Launch Interactive 3D Knowledge Graph](https://mchittineni.github.io/ultimate-ai-engineering-guide/)**

**Features:**

- 🌌 **3D Space Environment:** Rotate, pan, and zoom through 190 nodes and 350 directional concept edges in WebGL space.
- ✨ **Animated Particle Links:** Visualizes concept flow across topics with directional light particle effects.
- 🎯 **3D Focus & Camera Animation:** Click any node to focus the camera directly on the question or topic cluster.
- 📖 **Slide-out Glassmorphism Info Panel:** Instant access to question metadata and direct links to the raw Markdown files on GitHub.

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

**205 questions** across **10 topics** - 🟢 101 Beginner · 🟡 62 Intermediate · 🔴 42 Advanced

### 🧱 Foundations & Models

| Topic                                                    | Questions | 🟢  | 🟡  | 🔴  | What it covers                                                                                   |
| -------------------------------------------------------- | --------- | --- | --- | --- | ------------------------------------------------------------------------------------------------ |
| **[LLM Fundamentals](./llm-fundamentals/README.md)**     | 20        | 10  | 6   | 4   | Core architectures, Transformer mechanics, self-attention, context windows, tokenization, KV…    |
| **[Prompt Engineering](./prompt-engineering/README.md)** | 20        | 10  | 6   | 4   | Zero/few-shot, Chain-of-Thought (CoT), Tree-of-Thoughts, ReAct, system prompts, structured JSON… |

### 🧠 Retrieval & Agentic Systems

| Topic                                                                | Questions | 🟢  | 🟡  | 🔴  | What it covers                                                                                    |
| -------------------------------------------------------------------- | --------- | --- | --- | --- | ------------------------------------------------------------------------------------------------- |
| **[RAG and Vector Databases](./rag-and-vector-databases/README.md)** | 20        | 10  | 6   | 4   | Embeddings, vector indexing (HNSW, IVFFlat), hybrid search, chunking strategies, re-ranking, and… |
| **[AI Agents and MCP](./ai-agents-and-mcp/README.md)**               | 20        | 10  | 6   | 4   | Agentic workflows, Model Context Protocol (MCP), function calling, tool use, memory persistence,… |

### ⚙️ Adaptation & System Design

| Topic                                                                    | Questions | 🟢  | 🟡  | 🔴  | What it covers                                                                                   |
| ------------------------------------------------------------------------ | --------- | --- | --- | --- | ------------------------------------------------------------------------------------------------ |
| **[Fine-Tuning and Adaptation](./fine-tuning-and-adaptation/README.md)** | 20        | 10  | 6   | 4   | PEFT, LoRA, QLoRA, RLHF, DPO, GRPO, quantization (GGUF, AWQ, GPTQ), model distillation, and…     |
| **[AI System Design](./ai-system-design/README.md)**                     | 20        | 10  | 6   | 4   | High-throughput inference, TTFT/TPOT, streaming (SSE), semantic caching, GPU resource planning,… |

### 📊 Operations & Quality

| Topic                                                                | Questions | 🟢  | 🟡  | 🔴  | What it covers                                                                                  |
| -------------------------------------------------------------------- | --------- | --- | --- | --- | ----------------------------------------------------------------------------------------------- |
| **[LLMOps and Production AI](./llmops-and-production-ai/README.md)** | 20        | 10  | 6   | 4   | Observability, prompt tracing, cost management, drift detection, CI/CD pipelines for prompts &… |
| **[Evaluation and Testing](./evaluation-and-testing/README.md)**     | 20        | 10  | 6   | 4   | LLM-as-a-Judge, Ragas metrics (Faithfulness, Relevance), benchmarks (MMLU, HumanEval), unit…    |

### 🛡️ Governance & Career Track

| Topic                                                                | Questions | 🟢  | 🟡  | 🔴  | What it covers                                                                            |
| -------------------------------------------------------------------- | --------- | --- | --- | --- | ----------------------------------------------------------------------------------------- |
| **[AI Safety and Governance](./ai-safety-and-governance/README.md)** | 25        | 11  | 8   | 6   | Data privacy, PII masking, guardrails (NeMo, Llama Guard), alignment tax, copyright, and… |
| **[Interview Experience](./interview-experience/README.md)**         | 20        | 10  | 6   | 4   | Role-specific interview blueprints (AI Engineer, FDE, AI Architect), portfolio project…   |

<!-- STATS:END -->

---

## 📖 All questions

Click any topic to expand its questions, sorted by difficulty level.

<!-- TOC:START -->

### 🧱 Foundations & Models

_40 questions_

<details>
<summary><b>LLM Fundamentals</b> · 20 questions · 🟢 10 🟡 6 🔴 4</summary>

[Open the LLM Fundamentals index →](./llm-fundamentals/README.md)

| No. | Question                                                                                                                                                                                              | Difficulty      |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 1   | [What is KV Cache and how does it speed up inference?](./llm-fundamentals/what-is-kv-cache-and-how-does-it-speed-up-inference.md)                                                                     | 🟡 Intermediate |
| 2   | [How does Grouped-Query Attention (GQA) differ from Multi-Head Attention (MHA)?](./llm-fundamentals/how-does-grouped-query-attention-gqa-differ-from-multi-head-attention-mha.md)                     | 🟡 Intermediate |
| 12  | [What is the difference between encoder-only, decoder-only, and encoder-decoder LLMs?](./llm-fundamentals/what-is-the-difference-between-encoder-only-decoder-only-and-encoder-decoder-llms.md)       | 🟢 Beginner     |
| 13  | [How does Byte-Pair Encoding (BPE) tokenization work?](./llm-fundamentals/how-does-byte-pair-encoding-bpe-tokenization-work.md)                                                                       | 🟢 Beginner     |
| 14  | [How do Rotary Position Embeddings (RoPE) and RoPE scaling work?](./llm-fundamentals/how-do-rotary-position-embeddings-rope-and-rope-scaling-work.md)                                                 | 🔴 Advanced     |
| 51  | [What is Temperature, Top-p, and Top-k sampling?](./llm-fundamentals/what-is-temperature-top-p-and-top-k-sampling.md)                                                                                 | 🟢 Beginner     |
| 52  | [What is the difference between greedy decoding and beam search?](./llm-fundamentals/what-is-the-difference-between-greedy-decoding-and-beam-search.md)                                               | 🟢 Beginner     |
| 53  | [What is a context window and how does it limit LLM processing?](./llm-fundamentals/what-is-a-context-window-and-how-does-it-limit-llm-processing.md)                                                 | 🟢 Beginner     |
| 54  | [How does Multi-Query Attention (MQA) differ from Multi-Head Attention?](./llm-fundamentals/how-does-multi-query-attention-mqa-differ-from-multi-head-attention.md)                                   | 🟡 Intermediate |
| 55  | [How does FlashAttention optimize memory and speed via tiling?](./llm-fundamentals/how-does-flashattention-optimize-memory-and-speed-via-tiling.md)                                                   | 🔴 Advanced     |
| 101 | [What is tokenization and why can't LLMs process raw string characters directly?](./llm-fundamentals/what-is-tokenization-and-why-cant-llms-process-raw-string-characters-directly.md)                | 🟢 Beginner     |
| 102 | [What is the difference between causal and bidirectional self-attention?](./llm-fundamentals/what-is-the-difference-between-causal-and-bidirectional-self-attention.md)                               | 🟢 Beginner     |
| 103 | [What is a logit and how is it converted to token probabilities via Softmax?](./llm-fundamentals/what-is-a-logit-and-how-is-it-converted-to-token-probabilities-via-softmax.md)                       | 🟢 Beginner     |
| 104 | [What is an attention mask and why is it needed during batch processing?](./llm-fundamentals/what-is-an-attention-mask-and-why-is-it-needed-during-batch-processing.md)                               | 🟢 Beginner     |
| 105 | [What is positional encoding and why do Transformers need it?](./llm-fundamentals/what-is-positional-encoding-and-why-do-transformers-need-it.md)                                                     | 🟢 Beginner     |
| 106 | [How do Mixture of Experts (MoE) architectures scale parameter count efficiently?](./llm-fundamentals/how-do-mixture-of-experts-moe-architectures-scale-parameter-count-efficiently.md)               | 🟡 Intermediate |
| 107 | [What is linear attention and how does it attempt to solve quadratic complexity?](./llm-fundamentals/what-is-linear-attention-and-how-does-it-attempt-to-solve-quadratic-complexity.md)               | 🟡 Intermediate |
| 108 | [How does sliding window attention (SWA) reduce memory usage in long-context models?](./llm-fundamentals/how-does-sliding-window-attention-swa-reduce-memory-usage-in-long-context-models.md)         | 🟡 Intermediate |
| 109 | [How do state space models (SSMs) like Mamba compare to Transformer self-attention?](./llm-fundamentals/how-do-state-space-models-ssms-like-mamba-compare-to-transformer-self-attention.md)           | 🔴 Advanced     |
| 110 | [How does Differential Attention work to suppress noise and improve long-context focus?](./llm-fundamentals/how-does-differential-attention-work-to-suppress-noise-and-improve-long-context-focus.md) | 🔴 Advanced     |

</details>

<details>
<summary><b>Prompt Engineering</b> · 20 questions · 🟢 10 🟡 6 🔴 4</summary>

[Open the Prompt Engineering index →](./prompt-engineering/README.md)

| No. | Question                                                                                                                                                                                                    | Difficulty      |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 3   | [How does ReAct (Reasoning and Acting) prompting work?](./prompt-engineering/how-does-react-reasoning-and-acting-prompting-work.md)                                                                         | 🟡 Intermediate |
| 15  | [What is the difference between zero-shot and few-shot prompting?](./prompt-engineering/what-is-the-difference-between-zero-shot-and-few-shot-prompting.md)                                                 | 🟢 Beginner     |
| 16  | [How does Chain-of-Thought (CoT) prompting improve LLM reasoning?](./prompt-engineering/how-does-chain-of-thought-cot-prompting-improve-llm-reasoning.md)                                                   | 🟢 Beginner     |
| 17  | [How do you enforce structured JSON outputs from an LLM?](./prompt-engineering/how-do-you-enforce-structured-json-outputs-from-an-llm.md)                                                                   | 🟡 Intermediate |
| 18  | [How does Tree-of-Thoughts (ToT) prompting differ from Chain-of-Thought?](./prompt-engineering/how-does-tree-of-thoughts-tot-prompting-differ-from-chain-of-thought.md)                                     | 🔴 Advanced     |
| 56  | [What is a system prompt and how does it steer model behavior?](./prompt-engineering/what-is-a-system-prompt-and-how-does-it-steer-model-behavior.md)                                                       | 🟢 Beginner     |
| 57  | [What is prompt leaking and how do you prevent it?](./prompt-engineering/what-is-prompt-leaking-and-how-do-you-prevent-it.md)                                                                               | 🟢 Beginner     |
| 58  | [How do role prompting and persona framing affect LLM outputs?](./prompt-engineering/how-do-role-prompting-and-persona-framing-affect-llm-outputs.md)                                                       | 🟢 Beginner     |
| 59  | [How do you design few-shot examples to prevent label bias?](./prompt-engineering/how-do-you-design-few-shot-examples-to-prevent-label-bias.md)                                                             | 🟡 Intermediate |
| 60  | [How does Skeleton-of-Thought (SoT) speed up generation via parallel decoding?](./prompt-engineering/how-does-skeleton-of-thought-sot-speed-up-generation-via-parallel-decoding.md)                         | 🔴 Advanced     |
| 111 | [What is prompt priming and how does it set expectations for LLM responses?](./prompt-engineering/what-is-prompt-priming-and-how-does-it-set-expectations-for-llm-responses.md)                             | 🟢 Beginner     |
| 112 | [What is negative prompting and how do you instruct models what not to do?](./prompt-engineering/what-is-negative-prompting-and-how-do-you-instruct-models-what-not-to-do.md)                               | 🟢 Beginner     |
| 113 | [What is meta-prompting and how can an LLM generate or optimize its own prompts?](./prompt-engineering/what-is-meta-prompting-and-how-can-an-llm-generate-or-optimize-its-own-prompts.md)                   | 🟢 Beginner     |
| 114 | [How do you format multi-turn dialogue histories for chat models?](./prompt-engineering/how-do-you-format-multi-turn-dialogue-histories-for-chat-models.md)                                                 | 🟢 Beginner     |
| 115 | [What is context window truncation and how do you handle overflow gracefully?](./prompt-engineering/what-is-context-window-truncation-and-how-do-you-handle-overflow-gracefully.md)                         | 🟢 Beginner     |
| 116 | [How does Directional Stimulus Prompting guide LLMs toward specific output aspects?](./prompt-engineering/how-does-directional-stimulus-prompting-guide-llms-toward-specific-output-aspects.md)             | 🟡 Intermediate |
| 117 | [How does Active Prompting dynamically select the best exemplars for few-shot learning?](./prompt-engineering/how-does-active-prompting-dynamically-select-the-best-exemplars-for-few-shot-learning.md)     | 🟡 Intermediate |
| 118 | [How does Automatic Prompt Engineer (APE) optimize prompt selection using search?](./prompt-engineering/how-does-automatic-prompt-engineer-ape-optimize-prompt-selection-using-search.md)                   | 🟡 Intermediate |
| 119 | [How does Graph-of-Thoughts (GoT) extend Tree-of-Thoughts for arbitrary network reasoning?](./prompt-engineering/how-does-graph-of-thoughts-got-extend-tree-of-thoughts-for-arbitrary-network-reasoning.md) | 🔴 Advanced     |
| 120 | [How do soft prompts and prompt tuning differ from discrete text prompts?](./prompt-engineering/how-do-soft-prompts-and-prompt-tuning-differ-from-discrete-text-prompts.md)                                 | 🔴 Advanced     |

</details>

### 🧠 Retrieval & Agentic Systems

_40 questions_

<details>
<summary><b>RAG and Vector Databases</b> · 20 questions · 🟢 10 🟡 6 🔴 4</summary>

[Open the RAG and Vector Databases index →](./rag-and-vector-databases/README.md)

| No. | Question                                                                                                                                                                                                                                        | Difficulty      |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 4   | [What is the difference between HNSW and IVFFlat vector indexes?](./rag-and-vector-databases/what-is-the-difference-between-hnsw-and-ivfflat-vector-indexes.md)                                                                                 | 🟡 Intermediate |
| 19  | [What is Retrieval-Augmented Generation (RAG) and why is it used?](./rag-and-vector-databases/what-is-retrieval-augmented-generation-rag-and-why-is-it-used.md)                                                                                 | 🟢 Beginner     |
| 20  | [How do dense and sparse vector embeddings differ?](./rag-and-vector-databases/how-do-dense-and-sparse-vector-embeddings-differ.md)                                                                                                             | 🟢 Beginner     |
| 21  | [How does hybrid search combine BM25 and vector embeddings?](./rag-and-vector-databases/how-does-hybrid-search-combine-bm25-and-vector-embeddings.md)                                                                                           | 🟡 Intermediate |
| 22  | [How do cross-encoder rerankers and late-interaction (ColBERT) models work?](./rag-and-vector-databases/how-do-cross-encoder-rerankers-and-late-interaction-colbert-models-work.md)                                                             | 🔴 Advanced     |
| 61  | [What is chunk size and chunk overlap in text splitting?](./rag-and-vector-databases/what-is-chunk-size-and-chunk-overlap-in-text-splitting.md)                                                                                                 | 🟢 Beginner     |
| 62  | [What is Cosine Similarity vs Euclidean Distance in vector search?](./rag-and-vector-databases/what-is-cosine-similarity-vs-euclidean-distance-in-vector-search.md)                                                                             | 🟢 Beginner     |
| 63  | [What is the 'Lost in the Middle' phenomenon in LLM retrieval?](./rag-and-vector-databases/what-is-the-lost-in-the-middle-phenomenon-in-llm-retrieval.md)                                                                                       | 🟢 Beginner     |
| 64  | [How does query rewriting and Hypothetical Document Embeddings (HyDE) work?](./rag-and-vector-databases/how-does-query-rewriting-and-hypothetical-document-embeddings-hyde-work.md)                                                             | 🟡 Intermediate |
| 65  | [How do GraphRAG and Knowledge Graphs enhance vector retrieval?](./rag-and-vector-databases/how-do-graphrag-and-knowledge-graphs-enhance-vector-retrieval.md)                                                                                   | 🔴 Advanced     |
| 121 | [What is an embedding model and how does vector dimension affect search quality?](./rag-and-vector-databases/what-is-an-embedding-model-and-how-does-vector-dimension-affect-search-quality.md)                                                 | 🟢 Beginner     |
| 122 | [What is semantic search and how does it differ from traditional keyword search?](./rag-and-vector-databases/what-is-semantic-search-and-how-does-it-differ-from-traditional-keyword-search.md)                                                 | 🟢 Beginner     |
| 123 | [What is document metadata filtering in vector databases?](./rag-and-vector-databases/what-is-document-metadata-filtering-in-vector-databases.md)                                                                                               | 🟢 Beginner     |
| 124 | [What is single-representation vs multi-representation document retrieval?](./rag-and-vector-databases/what-is-single-representation-vs-multi-representation-document-retrieval.md)                                                             | 🟢 Beginner     |
| 125 | [What is document parsing and why do table formats break standard text splitters?](./rag-and-vector-databases/what-is-document-parsing-and-why-do-table-formats-break-standard-text-splitters.md)                                               | 🟢 Beginner     |
| 126 | [How does Parent-Document Retrieval link fine-grained vector chunks back to full parent context?](./rag-and-vector-databases/how-does-parent-document-retrieval-link-fine-grained-vector-chunks-back-to-full-parent-context.md)                 | 🟡 Intermediate |
| 127 | [How does Reciprocal Rank Fusion (RRF) combine scores from sparse and dense retrievers?](./rag-and-vector-databases/how-does-reciprocal-rank-fusion-rrf-combine-scores-from-sparse-and-dense-retrievers.md)                                     | 🟡 Intermediate |
| 128 | [How does contextual compression reduce context window token usage during RAG?](./rag-and-vector-databases/how-does-contextual-compression-reduce-context-window-token-usage-during-rag.md)                                                     | 🟡 Intermediate |
| 129 | [How does RAPTOR perform hierarchical tree-organized retrieval?](./rag-and-vector-databases/how-does-raptor-perform-hierarchical-tree-organized-retrieval.md)                                                                                   | 🔴 Advanced     |
| 130 | [How does Self-RAG train models to dynamically decide when to retrieve, evaluate, and critique documents?](./rag-and-vector-databases/how-does-self-rag-train-models-to-dynamically-decide-when-to-retrieve-evaluate-and-critique-documents.md) | 🔴 Advanced     |

</details>

<details>
<summary><b>AI Agents and MCP</b> · 20 questions · 🟢 10 🟡 6 🔴 4</summary>

[Open the AI Agents and MCP index →](./ai-agents-and-mcp/README.md)

| No. | Question                                                                                                                                                                                                           | Difficulty      |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------- |
| 5   | [What is the Model Context Protocol (MCP) and how does it work?](./ai-agents-and-mcp/what-is-the-model-context-protocol-mcp-and-how-does-it-work.md)                                                               | 🟡 Intermediate |
| 23  | [What is an AI agent and how does it differ from a standard LLM?](./ai-agents-and-mcp/what-is-an-ai-agent-and-how-does-it-differ-from-a-standard-llm.md)                                                           | 🟢 Beginner     |
| 24  | [How does LLM tool use and function calling work?](./ai-agents-and-mcp/how-does-llm-tool-use-and-function-calling-work.md)                                                                                         | 🟢 Beginner     |
| 25  | [How do you manage short-term and long-term memory in AI agents?](./ai-agents-and-mcp/how-do-you-manage-short-term-and-long-term-memory-in-ai-agents.md)                                                           | 🟡 Intermediate |
| 26  | [How do multi-agent architectures and hierarchical delegation work?](./ai-agents-and-mcp/how-do-multi-agent-architectures-and-hierarchical-delegation-work.md)                                                     | 🔴 Advanced     |
| 66  | [What is the ReAct loop (Thought, Action, Observation)?](./ai-agents-and-mcp/what-is-the-react-loop-thought-action-observation.md)                                                                                 | 🟢 Beginner     |
| 67  | [What is an MCP Tool vs an MCP Resource in Model Context Protocol?](./ai-agents-and-mcp/what-is-an-mcp-tool-vs-an-mcp-resource-in-model-context-protocol.md)                                                       | 🟢 Beginner     |
| 68  | [How do you handle tool execution errors in agentic loops?](./ai-agents-and-mcp/how-do-you-handle-tool-execution-errors-in-agentic-loops.md)                                                                       | 🟢 Beginner     |
| 69  | [How does MCP server-client architecture standardize context connections?](./ai-agents-and-mcp/how-does-mcp-server-client-architecture-standardize-context-connections.md)                                         | 🟡 Intermediate |
| 70  | [How do you prevent infinite agentic loops and runaway execution?](./ai-agents-and-mcp/how-do-you-prevent-infinite-agentic-loops-and-runaway-execution.md)                                                         | 🔴 Advanced     |
| 131 | [What is an agent tool schema and how do parameters get validated before invocation?](./ai-agents-and-mcp/what-is-an-agent-tool-schema-and-how-do-parameters-get-validated-before-invocation.md)                   | 🟢 Beginner     |
| 132 | [What is an agent state machine and how does state persist across multi-step execution?](./ai-agents-and-mcp/what-is-an-agent-state-machine-and-how-does-state-persist-across-multi-step-execution.md)             | 🟢 Beginner     |
| 133 | [What is human-in-the-loop (HITL) approval in autonomous agent workflows?](./ai-agents-and-mcp/what-is-human-in-the-loop-hitl-approval-in-autonomous-agent-workflows.md)                                           | 🟢 Beginner     |
| 134 | [What is synchronous vs asynchronous tool execution in AI agents?](./ai-agents-and-mcp/what-is-synchronous-vs-asynchronous-tool-execution-in-ai-agents.md)                                                         | 🟢 Beginner     |
| 135 | [What is an agent system prompt and how does it define tool availability?](./ai-agents-and-mcp/what-is-an-agent-system-prompt-and-how-does-it-define-tool-availability.md)                                         | 🟢 Beginner     |
| 136 | [How does Plan-and-Solve prompting decompose complex tasks into explicit execution sub-goals?](./ai-agents-and-mcp/how-does-plan-and-solve-prompting-decompose-complex-tasks-into-explicit-execution-sub-goals.md) | 🟡 Intermediate |
| 137 | [How does Agentic Search handle real-time pagination and query refinement?](./ai-agents-and-mcp/how-does-agentic-search-handle-real-time-pagination-and-query-refinement.md)                                       | 🟡 Intermediate |
| 138 | [How does MCP handle streaming updates and progress reporting from long-running tools?](./ai-agents-and-mcp/how-does-mcp-handle-streaming-updates-and-progress-reporting-from-long-running-tools.md)               | 🟡 Intermediate |
| 139 | [How do DAG-based Multi-Agent Orchestrators prevent state deadlocks?](./ai-agents-and-mcp/how-do-dag-based-multi-agent-orchestrators-prevent-state-deadlocks.md)                                                   | 🔴 Advanced     |
| 140 | [How do sandbox execution environments secure Code Interpreter tools?](./ai-agents-and-mcp/how-do-sandbox-execution-environments-secure-code-interpreter-tools.md)                                                 | 🔴 Advanced     |

</details>

### ⚙️ Adaptation & System Design

_40 questions_

<details>
<summary><b>Fine-Tuning and Adaptation</b> · 20 questions · 🟢 10 🟡 6 🔴 4</summary>

[Open the Fine-Tuning and Adaptation index →](./fine-tuning-and-adaptation/README.md)

| No. | Question                                                                                                                                                                                                                                | Difficulty      |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 6   | [What is LoRA and QLoRA for efficient fine-tuning?](./fine-tuning-and-adaptation/what-is-lora-and-qlora-for-efficient-fine-tuning.md)                                                                                                   | 🟡 Intermediate |
| 27  | [What is the difference between pre-training, fine-tuning, and in-context learning?](./fine-tuning-and-adaptation/what-is-the-difference-between-pre-training-fine-tuning-and-in-context-learning.md)                                   | 🟢 Beginner     |
| 28  | [What is quantization and how do INT8 and INT4 reduce LLM footprint?](./fine-tuning-and-adaptation/what-is-quantization-and-how-do-int8-and-int4-reduce-llm-footprint.md)                                                               | 🟢 Beginner     |
| 29  | [How does Direct Preference Optimization (DPO) differ from RLHF?](./fine-tuning-and-adaptation/how-does-direct-preference-optimization-dpo-differ-from-rlhf.md)                                                                         | 🟡 Intermediate |
| 30  | [How does Group Relative Policy Optimization (GRPO) work in DeepSeek R1?](./fine-tuning-and-adaptation/how-does-group-relative-policy-optimization-grpo-work-in-deepseek-r1.md)                                                         | 🔴 Advanced     |
| 71  | [What is Supervised Fine-Tuning (SFT) and when is it required?](./fine-tuning-and-adaptation/what-is-supervised-fine-tuning-sft-and-when-is-it-required.md)                                                                             | 🟢 Beginner     |
| 72  | [What is catastrophic forgetting during LLM fine-tuning?](./fine-tuning-and-adaptation/what-is-catastrophic-forgetting-during-llm-fine-tuning.md)                                                                                       | 🟢 Beginner     |
| 73  | [What is LoRA rank r and alpha scaling factor?](./fine-tuning-and-adaptation/what-is-lora-rank-r-and-alpha-scaling-factor.md)                                                                                                           | 🟢 Beginner     |
| 74  | [How does model distillation transfer knowledge from teacher to student?](./fine-tuning-and-adaptation/how-does-model-distillation-transfer-knowledge-from-teacher-to-student.md)                                                       | 🟡 Intermediate |
| 75  | [How does Kahneman-Tversky Optimization (KTO) differ from DPO?](./fine-tuning-and-adaptation/how-does-kahneman-tversky-optimization-kto-differ-from-dpo.md)                                                                             | 🔴 Advanced     |
| 141 | [What is dataset formatting for instruction tuning (Alpaca vs ShareGPT formats)?](./fine-tuning-and-adaptation/what-is-dataset-formatting-for-instruction-tuning-alpaca-vs-sharegpt-formats.md)                                         | 🟢 Beginner     |
| 142 | [What is learning rate scheduling (cosine decay) during LLM fine-tuning?](./fine-tuning-and-adaptation/what-is-learning-rate-scheduling-cosine-decay-during-llm-fine-tuning.md)                                                         | 🟢 Beginner     |
| 143 | [What is gradient accumulation and how does it simulate larger batch sizes on small GPUs?](./fine-tuning-and-adaptation/what-is-gradient-accumulation-and-how-does-it-simulate-larger-batch-sizes-on-small-gpus.md)                     | 🟢 Beginner     |
| 144 | [What is mixed precision training (FP16 vs BF16) and why is BF16 preferred on modern GPUs?](./fine-tuning-and-adaptation/what-is-mixed-precision-training-fp16-vs-bf16-and-why-is-bf16-preferred-on-modern-gpus.md)                     | 🟢 Beginner     |
| 145 | [What is weight merging in LoRA and why does it eliminate inference latency penalties?](./fine-tuning-and-adaptation/what-is-weight-merging-in-lora-and-why-does-it-eliminate-inference-latency-penalties.md)                           | 🟢 Beginner     |
| 146 | [How does DoRA (Weight-Decomposed Low-Rank Adaptation) improve directional weight updates over LoRA?](./fine-tuning-and-adaptation/how-does-dora-weight-decomposed-low-rank-adaptation-improve-directional-weight-updates-over-lora.md) | 🟡 Intermediate |
| 147 | [How does GGUF format enable quantization and CPU/GPU offloading in llama.cpp?](./fine-tuning-and-adaptation/how-does-gguf-format-enable-quantization-and-cpu-gpu-offloading-in-llama-cpp.md)                                           | 🟡 Intermediate |
| 148 | [How does AWQ (Activation-aware Weight Quantization) preserve critical weights compared to GPTQ?](./fine-tuning-and-adaptation/how-does-awq-activation-aware-weight-quantization-preserve-critical-weights-compared-to-gptq.md)         | 🟡 Intermediate |
| 149 | [How does ORPO perform SFT and alignment in a single step without reference models?](./fine-tuning-and-adaptation/how-does-orpo-perform-sft-and-alignment-in-a-single-step-without-reference-models.md)                                 | 🔴 Advanced     |
| 150 | [How does DeepSpeed ZeRO stage 1, 2, and 3 partition optimizer states, gradients, and parameters?](./fine-tuning-and-adaptation/how-does-deepspeed-zero-stage-1-2-and-3-partition-optimizer-states-gradients-and-parameters.md)         | 🔴 Advanced     |

</details>

<details>
<summary><b>AI System Design</b> · 20 questions · 🟢 10 🟡 6 🔴 4</summary>

[Open the AI System Design index →](./ai-system-design/README.md)

| No. | Question                                                                                                                                                                                                                                          | Difficulty      |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 7   | [How do you optimize Time to First Token (TTFT) vs Time Per Output Token (TPOT)?](./ai-system-design/how-do-you-optimize-time-to-first-token-ttft-vs-time-per-output-token-tpot.md)                                                               | 🟡 Intermediate |
| 31  | [What is Server-Sent Events (SSE) streaming for LLM responses?](./ai-system-design/what-is-server-sent-events-sse-streaming-for-llm-responses.md)                                                                                                 | 🟢 Beginner     |
| 32  | [How does semantic caching reduce LLM API latency and cost?](./ai-system-design/how-does-semantic-caching-reduce-llm-api-latency-and-cost.md)                                                                                                     | 🟢 Beginner     |
| 33  | [How does PagedAttention in vLLM solve memory fragmentation?](./ai-system-design/how-does-pagedattention-in-vllm-solve-memory-fragmentation.md)                                                                                                   | 🟡 Intermediate |
| 34  | [How does speculative decoding speed up LLM inference?](./ai-system-design/how-does-speculative-decoding-speed-up-llm-inference.md)                                                                                                               | 🔴 Advanced     |
| 76  | [What is continuous batching and how does it improve GPU utilization?](./ai-system-design/what-is-continuous-batching-and-how-does-it-improve-gpu-utilization.md)                                                                                 | 🟢 Beginner     |
| 77  | [What is the difference between prefill phase and decoding phase?](./ai-system-design/what-is-the-difference-between-prefill-phase-and-decoding-phase.md)                                                                                         | 🟢 Beginner     |
| 78  | [What is GPU VRAM bandwidth and why is decoding memory-bound?](./ai-system-design/what-is-gpu-vram-bandwidth-and-why-is-decoding-memory-bound.md)                                                                                                 | 🟢 Beginner     |
| 79  | [How do you design a multi-tenant LLM gateway with rate limits?](./ai-system-design/how-do-you-design-a-multi-tenant-llm-gateway-with-rate-limits.md)                                                                                             | 🟡 Intermediate |
| 80  | [How does chunked prefill disaggregate prefill and decoding nodes?](./ai-system-design/how-does-chunked-prefill-disaggregate-prefill-and-decoding-nodes.md)                                                                                       | 🔴 Advanced     |
| 151 | [What is load balancing for LLM inference clusters across multi-region GPU pools?](./ai-system-design/what-is-load-balancing-for-llm-inference-clusters-across-multi-region-gpu-pools.md)                                                         | 🟢 Beginner     |
| 152 | [What is prefix caching (prompt caching) and how does it eliminate redundant KV computation?](./ai-system-design/what-is-prefix-caching-prompt-caching-and-how-does-it-eliminate-redundant-kv-computation.md)                                     | 🟢 Beginner     |
| 153 | [What is an LLM router and how does it dynamically direct queries based on complexity?](./ai-system-design/what-is-an-llm-router-and-how-does-it-dynamically-direct-queries-based-on-complexity.md)                                               | 🟢 Beginner     |
| 154 | [What is connection pooling and keep-alive strategy for high-throughput LLM streaming APIs?](./ai-system-design/what-is-connection-pooling-and-keep-alive-strategy-for-high-throughput-llm-streaming-apis.md)                                     | 🟢 Beginner     |
| 155 | [What is graceful degradation in AI services when model providers experience downtime?](./ai-system-design/what-is-graceful-degradation-in-ai-services-when-model-providers-experience-downtime.md)                                               | 🟢 Beginner     |
| 156 | [How does Chunked Prefill prevent decoding latency spikes during concurrent batch processing?](./ai-system-design/how-does-chunked-prefill-prevent-decoding-latency-spikes-during-concurrent-batch-processing.md)                                 | 🟡 Intermediate |
| 157 | [How do tensor parallelism (TP) and pipeline parallelism (PP) split large model weights across multi-GPU nodes?](./ai-system-design/how-do-tensor-parallelism-tp-and-pipeline-parallelism-pp-split-large-model-weights-across-multi-gpu-nodes.md) | 🟡 Intermediate |
| 158 | [How does Medusa multi-head decoding accelerate inference without a separate draft model?](./ai-system-design/how-does-medusa-multi-head-decoding-accelerate-inference-without-a-separate-draft-model.md)                                         | 🟡 Intermediate |
| 159 | [How does vLLM PagedAttention manage Virtual Memory Pages to eliminate KV cache fragmentation?](./ai-system-design/how-does-vllm-pagedattention-manage-virtual-memory-pages-to-eliminate-kv-cache-fragmentation.md)                               | 🔴 Advanced     |
| 160 | [How to design a global multi-region AI inference architecture with sub-100ms TTFT SLAs?](./ai-system-design/how-to-design-a-global-multi-region-ai-inference-architecture-with-sub-100ms-ttft-slas.md)                                           | 🔴 Advanced     |

</details>

### 📊 Operations & Quality

_40 questions_

<details>
<summary><b>LLMOps and Production AI</b> · 20 questions · 🟢 10 🟡 6 🔴 4</summary>

[Open the LLMOps and Production AI index →](./llmops-and-production-ai/README.md)

| No. | Question                                                                                                                                                                                                                                                      | Difficulty      |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 8   | [How do you implement distributed tracing for multi-step LLM pipelines?](./llmops-and-production-ai/how-do-you-implement-distributed-tracing-for-multi-step-llm-pipelines.md)                                                                                 | 🟡 Intermediate |
| 35  | [What is LLMOps and how does it differ from traditional MLOps?](./llmops-and-production-ai/what-is-llmops-and-how-does-it-differ-from-traditional-mlops.md)                                                                                                   | 🟢 Beginner     |
| 36  | [How do you monitor LLM token usage, latency, and costs in production?](./llmops-and-production-ai/how-do-you-monitor-llm-token-usage-latency-and-costs-in-production.md)                                                                                     | 🟢 Beginner     |
| 37  | [How do you implement fallback routing and rate limiting for LLM APIs?](./llmops-and-production-ai/how-do-you-implement-fallback-routing-and-rate-limiting-for-llm-apis.md)                                                                                   | 🟡 Intermediate |
| 38  | [How do you detect and mitigate data and concept drift in production LLMs?](./llmops-and-production-ai/how-do-you-detect-and-mitigate-data-and-concept-drift-in-production-llms.md)                                                                           | 🔴 Advanced     |
| 81  | [What is prompt versioning and why is it essential?](./llmops-and-production-ai/what-is-prompt-versioning-and-why-is-it-essential.md)                                                                                                                         | 🟢 Beginner     |
| 82  | [What is an OpenTelemetry span in LLM tracing?](./llmops-and-production-ai/what-is-an-opentelemetry-span-in-llm-tracing.md)                                                                                                                                   | 🟢 Beginner     |
| 83  | [How do you budget and cap monthly LLM API costs?](./llmops-and-production-ai/how-do-you-budget-and-cap-monthly-llm-api-costs.md)                                                                                                                             | 🟢 Beginner     |
| 84  | [How do you build a canary deployment pipeline for prompt updates?](./llmops-and-production-ai/how-do-you-build-a-canary-deployment-pipeline-for-prompt-updates.md)                                                                                           | 🟡 Intermediate |
| 85  | [How do you architect real-time anomaly detection for rogue agent spends?](./llmops-and-production-ai/how-do-you-architect-real-time-anomaly-detection-for-rogue-agent-spends.md)                                                                             | 🔴 Advanced     |
| 161 | [What is structured logging for LLM prompts, completions, and token metrics?](./llmops-and-production-ai/what-is-structured-logging-for-llm-prompts-completions-and-token-metrics.md)                                                                         | 🟢 Beginner     |
| 162 | [What is cost attribution modeling per user, team, and organization in LLM applications?](./llmops-and-production-ai/what-is-cost-attribution-modeling-per-user-team-and-organization-in-llm-applications.md)                                                 | 🟢 Beginner     |
| 163 | [What is SLA/SLO monitoring for Time-to-First-Token (TTFT) and throughput (Tokens/sec)?](./llmops-and-production-ai/what-is-sla-slo-monitoring-for-time-to-first-token-ttft-and-throughput-tokens-sec.md)                                                     | 🟢 Beginner     |
| 164 | [What is semantic versioning for prompts and model configurations in production deployments?](./llmops-and-production-ai/what-is-semantic-versioning-for-prompts-and-model-configurations-in-production-deployments.md)                                       | 🟢 Beginner     |
| 165 | [What is fallback configuration when primary LLM providers return 5xx errors?](./llmops-and-production-ai/what-is-fallback-configuration-when-primary-llm-providers-return-5xx-errors.md)                                                                     | 🟢 Beginner     |
| 166 | [How do you set up automated prompt regression pipelines in GitHub Actions CI/CD?](./llmops-and-production-ai/how-do-you-set-up-automated-prompt-regression-pipelines-in-github-actions-ci-cd.md)                                                             | 🟡 Intermediate |
| 167 | [How to detect semantic drift in user queries using embedding clustering over time?](./llmops-and-production-ai/how-to-detect-semantic-drift-in-user-queries-using-embedding-clustering-over-time.md)                                                         | 🟡 Intermediate |
| 168 | [How to build a continuous evaluation pipeline sampling production traces for human review?](./llmops-and-production-ai/how-to-build-a-continuous-evaluation-pipeline-sampling-production-traces-for-human-review.md)                                         | 🟡 Intermediate |
| 169 | [How to design an enterprise-grade LLM Gateway with dynamic fallback, tenant rate limiting, and cost allocation?](./llmops-and-production-ai/how-to-design-an-enterprise-grade-llm-gateway-with-dynamic-fallback-tenant-rate-limiting-and-cost-allocation.md) | 🔴 Advanced     |
| 170 | [How to handle confidential enterprise telemetry and PII sanitization in compliance-heavy industries?](./llmops-and-production-ai/how-to-handle-confidential-enterprise-telemetry-and-pii-sanitization-in-compliance-heavy-industries.md)                     | 🔴 Advanced     |

</details>

<details>
<summary><b>Evaluation and Testing</b> · 20 questions · 🟢 10 🟡 6 🔴 4</summary>

[Open the Evaluation and Testing index →](./evaluation-and-testing/README.md)

| No. | Question                                                                                                                                                                                                                        | Difficulty      |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 9   | [How do Faithfulness, Context Recall, and Answer Relevance differ in Ragas?](./evaluation-and-testing/how-do-faithfulness-context-recall-and-answer-relevance-differ-in-ragas.md)                                               | 🟡 Intermediate |
| 39  | [What is LLM-as-a-Judge and how is it used for automated evaluations?](./evaluation-and-testing/what-is-llm-as-a-judge-and-how-is-it-used-for-automated-evaluations.md)                                                         | 🟢 Beginner     |
| 40  | [What are standard LLM benchmarks like MMLU, GSM8K, and HumanEval?](./evaluation-and-testing/what-are-standard-llm-benchmarks-like-mmlu-gsm8k-and-humaneval.md)                                                                 | 🟢 Beginner     |
| 41  | [How do you build a CI/CD prompt regression testing suite?](./evaluation-and-testing/how-do-you-build-a-ci-cd-prompt-regression-testing-suite.md)                                                                               | 🟡 Intermediate |
| 42  | [How do you mitigate positional bias and self-preference in LLM-as-a-Judge?](./evaluation-and-testing/how-do-you-mitigate-positional-bias-and-self-preference-in-llm-as-a-judge.md)                                             | 🔴 Advanced     |
| 86  | [What is context precision vs context recall in RAG?](./evaluation-and-testing/what-is-context-precision-vs-context-recall-in-rag.md)                                                                                           | 🟢 Beginner     |
| 87  | [What is faithfulness vs answer relevance in LLM evals?](./evaluation-and-testing/what-is-faithfulness-vs-answer-relevance-in-llm-evals.md)                                                                                     | 🟢 Beginner     |
| 88  | [What is ground-truth reference data in evaluation harnesses?](./evaluation-and-testing/what-is-ground-truth-reference-data-in-evaluation-harnesses.md)                                                                         | 🟢 Beginner     |
| 89  | [How do you measure inter-annotator agreement (Cohen's Kappa) with LLM judges?](./evaluation-and-testing/how-do-you-measure-inter-annotator-agreement-cohens-kappa-with-llm-judges.md)                                          | 🟡 Intermediate |
| 90  | [How do you build an automated red teaming harness against jailbreaks?](./evaluation-and-testing/how-do-you-build-an-automated-red-teaming-harness-against-jailbreaks.md)                                                       | 🔴 Advanced     |
| 171 | [What is exact match (EM) vs F1 score in extraction and classification evals?](./evaluation-and-testing/what-is-exact-match-em-vs-f1-score-in-extraction-and-classification-evals.md)                                           | 🟢 Beginner     |
| 172 | [What is BLEU and ROUGE scoring and why are they inadequate for modern LLM evaluation?](./evaluation-and-testing/what-is-bleu-and-rouge-scoring-and-why-are-they-inadequate-for-modern-llm-evaluation.md)                       | 🟢 Beginner     |
| 173 | [What is assertion testing in LLM unit tests?](./evaluation-and-testing/what-is-assertion-testing-in-llm-unit-tests.md)                                                                                                         | 🟢 Beginner     |
| 174 | [What is synthetic evaluation dataset generation and when should you use it?](./evaluation-and-testing/what-is-synthetic-evaluation-dataset-generation-and-when-should-you-use-it.md)                                           | 🟢 Beginner     |
| 175 | [What is human evaluation (RLHF human rating) and how do you design annotation rubrics?](./evaluation-and-testing/what-is-human-evaluation-rlhf-human-rating-and-how-do-you-design-annotation-rubrics.md)                       | 🟢 Beginner     |
| 176 | [How to measure model hallucination rate using NLI (Natural Language Inference) entailment models?](./evaluation-and-testing/how-to-measure-model-hallucination-rate-using-nli-natural-language-inference-entailment-models.md) | 🟡 Intermediate |
| 177 | [How to mitigate Verbosity Bias and Position Bias in LLM-as-a-Judge evaluations?](./evaluation-and-testing/how-to-mitigate-verbosity-bias-and-position-bias-in-llm-as-a-judge-evaluations.md)                                   | 🟡 Intermediate |
| 178 | [How to build an automated RAG evaluation harness measuring Context Precision and Recall?](./evaluation-and-testing/how-to-build-an-automated-rag-evaluation-harness-measuring-context-precision-and-recall.md)                 | 🟡 Intermediate |
| 179 | [How to implement Elo rating systems to benchmark model performance?](./evaluation-and-testing/how-to-implement-elo-rating-systems-to-benchmark-model-performance.md)                                                           | 🔴 Advanced     |
| 180 | [How to build automated adversarial red teaming engines to discover safety guardrail bypasses?](./evaluation-and-testing/how-to-build-automated-adversarial-red-teaming-engines-to-discover-safety-guardrail-bypasses.md)       | 🔴 Advanced     |

</details>

### 🛡️ Governance & Career Track

_45 questions_

<details>
<summary><b>AI Safety and Governance</b> · 25 questions · 🟢 11 🟡 8 🔴 6</summary>

[Open the AI Safety and Governance index →](./ai-safety-and-governance/README.md)

| No. | Question                                                                                                                                                                                                                                  | Difficulty      |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 10  | [How do input and output guardrails prevent jailbreaks and data leaks?](./ai-safety-and-governance/how-do-input-and-output-guardrails-prevent-jailbreaks-and-data-leaks.md)                                                               | 🟡 Intermediate |
| 43  | [What is prompt injection and how does it differ from SQL injection?](./ai-safety-and-governance/what-is-prompt-injection-and-how-does-it-differ-from-sql-injection.md)                                                                   | 🟢 Beginner     |
| 44  | [How do you redact PII (Personally Identifiable Information) before sending prompts to LLMs?](./ai-safety-and-governance/how-do-you-redact-pii-personally-identifiable-information-before-sending-prompts-to-llms.md)                     | 🟢 Beginner     |
| 45  | [How does Llama Guard classify unsafe inputs and outputs?](./ai-safety-and-governance/how-does-llama-guard-classify-unsafe-inputs-and-outputs.md)                                                                                         | 🟡 Intermediate |
| 46  | [What is the alignment tax and how does it impact model reasoning?](./ai-safety-and-governance/what-is-the-alignment-tax-and-how-does-it-impact-model-reasoning.md)                                                                       | 🔴 Advanced     |
| 91  | [What is system prompt exfiltration and how to prevent it?](./ai-safety-and-governance/what-is-system-prompt-exfiltration-and-how-to-prevent-it.md)                                                                                       | 🟢 Beginner     |
| 92  | [What is data exfiltration via LLM tool calls?](./ai-safety-and-governance/what-is-data-exfiltration-via-llm-tool-calls.md)                                                                                                               | 🟢 Beginner     |
| 93  | [What is hallucination and what are its primary causes?](./ai-safety-and-governance/what-is-hallucination-and-what-are-its-primary-causes.md)                                                                                             | 🟢 Beginner     |
| 94  | [How do NeMo Guardrails enforce programmable rails using Colang?](./ai-safety-and-governance/how-do-nemo-guardrails-enforce-programmable-rails-using-colang.md)                                                                           | 🟡 Intermediate |
| 95  | [How do you enforce strict RBAC and data isolation in enterprise RAG?](./ai-safety-and-governance/how-do-you-enforce-strict-rbac-and-data-isolation-in-enterprise-rag.md)                                                                 | 🔴 Advanced     |
| 181 | [What is indirect prompt injection and how does it occur when parsing web pages/documents?](./ai-safety-and-governance/what-is-indirect-prompt-injection-and-how-does-it-occur-when-parsing-web-pages-documents.md)                       | 🟢 Beginner     |
| 182 | [What is PII masking (pseudonymization) and how do Presidio/Regex filters protect user privacy?](./ai-safety-and-governance/what-is-pii-masking-pseudonymization-and-how-do-presidio-regex-filters-protect-user-privacy.md)               | 🟢 Beginner     |
| 183 | [What is copyright infringement risk in RAG and fine-tuning datasets?](./ai-safety-and-governance/what-is-copyright-infringement-risk-in-rag-and-fine-tuning-datasets.md)                                                                 | 🟢 Beginner     |
| 184 | [What is model jailbreaking and how do safety classifiers block it?](./ai-safety-and-governance/what-is-model-jailbreaking-and-how-do-safety-classifiers-block-it.md)                                                                     | 🟢 Beginner     |
| 185 | [What is data lineage tracking for RAG documents and enterprise vector stores?](./ai-safety-and-governance/what-is-data-lineage-tracking-for-rag-documents-and-enterprise-vector-stores.md)                                               | 🟢 Beginner     |
| 186 | [How to prevent Data Exfiltration via Markdown image tags and hidden web beacons in LLM outputs?](./ai-safety-and-governance/how-to-prevent-data-exfiltration-via-markdown-image-tags-and-hidden-web-beacons-in-llm-outputs.md)           | 🟡 Intermediate |
| 187 | [How does Llama Guard taxonomy classify unsafe inputs and outputs across safety categories?](./ai-safety-and-governance/how-does-llama-guard-taxonomy-classify-unsafe-inputs-and-outputs-across-safety-categories.md)                     | 🟡 Intermediate |
| 188 | [How to enforce Role-Based Access Control (RBAC) filtering in multi-tenant RAG vector search?](./ai-safety-and-governance/how-to-enforce-role-based-access-control-rbac-filtering-in-multi-tenant-rag-vector-search.md)                   | 🟡 Intermediate |
| 189 | [How do NeMo Guardrails use Colang state flows to strictly control conversation trajectories?](./ai-safety-and-governance/how-do-nemo-guardrails-use-colang-state-flows-to-strictly-control-conversation-trajectories.md)                 | 🔴 Advanced     |
| 190 | [How to audit and secure Model Context Protocol (MCP) servers against unauthorized tool invocation?](./ai-safety-and-governance/how-to-audit-and-secure-model-context-protocol-mcp-servers-against-unauthorized-tool-invocation.md)       | 🔴 Advanced     |
| 201 | [What is model inversion and membership inference, and how do you defend against them?](./ai-safety-and-governance/what-is-model-inversion-and-membership-inference-and-how-do-you-defend-against-them.md)                                | 🔴 Advanced     |
| 202 | [What is training data poisoning and how do backdoor triggers survive fine-tuning?](./ai-safety-and-governance/what-is-training-data-poisoning-and-how-do-backdoor-triggers-survive-fine-tuning.md)                                       | 🔴 Advanced     |
| 203 | [What is model supply chain security and why are serialized model weights dangerous?](./ai-safety-and-governance/what-is-model-supply-chain-security-and-why-are-serialized-model-weights-dangerous.md)                                   | 🟡 Intermediate |
| 204 | [How does the EU AI Act classify AI systems into risk tiers?](./ai-safety-and-governance/how-does-the-eu-ai-act-classify-ai-systems-into-risk-tiers.md)                                                                                   | 🟡 Intermediate |
| 205 | [What is the NIST AI Risk Management Framework and how do its four functions structure AI governance?](./ai-safety-and-governance/what-is-the-nist-ai-risk-management-framework-and-how-do-its-four-functions-structure-ai-governance.md) | 🟢 Beginner     |

</details>

<details>
<summary><b>Interview Experience</b> · 20 questions · 🟢 10 🟡 6 🔴 4</summary>

[Open the Interview Experience index →](./interview-experience/README.md)

| No. | Question                                                                                                                                                                                                                              | Difficulty      |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 11  | [What are the key differences between AI Engineer, ML Engineer, and FDE roles?](./interview-experience/what-are-the-key-differences-between-ai-engineer-ml-engineer-and-fde-roles.md)                                                 | 🟡 Intermediate |
| 47  | [How do you prepare for an AI engineering coding interview?](./interview-experience/how-do-you-prepare-for-an-ai-engineering-coding-interview.md)                                                                                     | 🟢 Beginner     |
| 48  | [How should you present an AI portfolio project to hiring managers?](./interview-experience/how-should-you-present-an-ai-portfolio-project-to-hiring-managers.md)                                                                     | 🟢 Beginner     |
| 49  | [How do you structure a system design interview response for an LLM application?](./interview-experience/how-do-you-structure-a-system-design-interview-response-for-an-llm-application.md)                                           | 🟡 Intermediate |
| 50  | [How do you handle scenario-based trade-off questions in senior AI engineering interviews?](./interview-experience/how-do-you-handle-scenario-based-trade-off-questions-in-senior-ai-engineering-interviews.md)                       | 🔴 Advanced     |
| 96  | [What are the most common pitfalls in AI engineering coding interviews?](./interview-experience/what-are-the-most-common-pitfalls-in-ai-engineering-coding-interviews.md)                                                             | 🟢 Beginner     |
| 97  | [How do you explain LLM hallucination mitigation to interviewers?](./interview-experience/how-do-you-explain-llm-hallucination-mitigation-to-interviewers.md)                                                                         | 🟢 Beginner     |
| 98  | [How do you demonstrate production readiness in a take-home AI project?](./interview-experience/how-do-you-demonstrate-production-readiness-in-a-take-home-ai-project.md)                                                             | 🟢 Beginner     |
| 99  | [How do you answer 'What is your favorite paper or technique in AI'?](./interview-experience/how-do-you-answer-what-is-your-favorite-paper-or-technique-in-ai.md)                                                                     | 🟡 Intermediate |
| 100 | [How do you lead an AI system architecture deep dive under ambiguity?](./interview-experience/how-do-you-lead-an-ai-system-architecture-deep-dive-under-ambiguity.md)                                                                 | 🔴 Advanced     |
| 191 | [How to prepare for an AI Engineer coding interview (raw SDK vs frameworks)?](./interview-experience/how-to-prepare-for-an-ai-engineer-coding-interview-raw-sdk-vs-frameworks.md)                                                     | 🟢 Beginner     |
| 192 | [How to structure an AI portfolio project to catch the eye of hiring managers?](./interview-experience/how-to-structure-an-ai-portfolio-project-to-catch-the-eye-of-hiring-managers.md)                                               | 🟢 Beginner     |
| 193 | [What are the core differences between AI Engineer, ML Engineer, and FDE roles?](./interview-experience/what-are-the-core-differences-between-ai-engineer-ml-engineer-and-fde-roles.md)                                               | 🟢 Beginner     |
| 194 | [How to answer scenario questions about trade-offs between RAG and Fine-Tuning?](./interview-experience/how-to-answer-scenario-questions-about-trade-offs-between-rag-and-fine-tuning.md)                                             | 🟢 Beginner     |
| 195 | [How to explain LLM hallucination mitigation in a system design interview?](./interview-experience/how-to-explain-llm-hallucination-mitigation-in-a-system-design-interview.md)                                                       | 🟢 Beginner     |
| 196 | [How to lead an ambiguous AI system design interview from requirements to architecture?](./interview-experience/how-to-lead-an-ambiguous-ai-system-design-interview-from-requirements-to-architecture.md)                             | 🟡 Intermediate |
| 197 | [How to handle live coding failures and non-deterministic model outputs during interviews?](./interview-experience/how-to-handle-live-coding-failures-and-non-deterministic-model-outputs-during-interviews.md)                       | 🟡 Intermediate |
| 198 | [How to demonstrate production-grade AI engineering rigor over toy notebook demos?](./interview-experience/how-to-demonstrate-production-grade-ai-engineering-rigor-over-toy-notebook-demos.md)                                       | 🟡 Intermediate |
| 199 | [How to conduct a complete system design interview for a multi-tenant enterprise RAG search platform?](./interview-experience/how-to-conduct-a-complete-system-design-interview-for-a-multi-tenant-enterprise-rag-search-platform.md) | 🔴 Advanced     |
| 200 | [How to design an autonomous multi-agent software engineering system in a staff-level interview?](./interview-experience/how-to-design-an-autonomous-multi-agent-software-engineering-system-in-a-staff-level-interview.md)           | 🔴 Advanced     |

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

### Local Development & Preview Workflow

```bash
# 1. Validate content and schema integrity
python3 scripts/validate_content.py

# 2. Inject cross-topic [[wikilinks]]
python3 scripts/inject_wikilinks.py

# 3. Regenerate index files and README stats
python3 scripts/generate_indexes.py

# 4. Build 3D Knowledge Graph HTML for GitHub Pages preview
python3 scripts/build_knowledge_graph.py

# 5. Preview locally in browser
open docs/index.html
```

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on adding new questions, running local validation tools, and maintaining index freshness.

---

## 📄 License

This repository is licensed under the [MIT License](./LICENSE).
