#!/usr/bin/env python3
"""Inject cross-topic [[wikilinks]] between related question files.

Scans all question files in the vault, identifies semantically related questions across
different topics based on shared concepts, tags, and key terms, and appends a structured
## Related Questions section with [[wikilinks]] (and relative markdown links for standard rendering).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))

from lib_content import REPO_ROOT, all_questions, load_topics, parse_frontmatter

# A `---` alone on its line, used as the footer rule at the end of a question file.
FOOTER_RULE_RE = re.compile(r"^---[ \t]*$", re.M)

# Semantic cross-topic concept mappings (by question ID pairs or target question IDs per category)
CROSS_LINK_MAP = {
    # LLM Fundamentals
    101: [13, 144, 121], # Tokenization -> BPE, Precision, Embeddings
    102: [12, 114, 105], # Causal vs Bidirectional -> Encoder/Decoder, Multi-turn, Positional Encoding
    103: [51, 142, 163], # Logits/Softmax -> Sampling, LR Scheduling, SLO Latency
    104: [143, 156, 107], # Attention Mask -> Batching/Grad Accum, Chunked Prefill, Linear Attn
    105: [14, 102, 108], # Positional Encoding -> RoPE, Causal Attn, SWA
    106: [157, 150, 147], # MoE -> Parallelism, ZeRO, GGUF
    107: [109, 159, 104], # Linear Attn -> Mamba SSM, PagedAttention, Attention Mask
    108: [152, 156, 128], # SWA -> Prefix Caching, Chunked Prefill, Contextual Compression
    109: [107, 159, 157], # Mamba SSM -> Linear Attn, PagedAttention, Parallelism
    110: [128, 176, 178], # Diff Attention -> Contextual Compression, NLI Hallucination, RAG Evals

    # Prompt Engineering
    111: [135, 164, 191], # Priming -> System Prompt, SemVer Prompts, SDK vs Frameworks
    112: [184, 173, 195], # Negative Prompting -> Jailbreaking, Assertion Evals, Hallucination Defense
    113: [118, 174, 136], # Meta-Prompting -> APE, Synthetic Evals, Plan-and-Solve
    114: [132, 138, 154], # Multi-turn -> State Machine, MCP Progress, Streaming Sockets
    115: [128, 152, 156], # Context Truncation -> Compression, Prefix Cache, Chunked Prefill
    116: [122, 127, 153], # Directional Stimulus -> Semantic Search, RRF, Router
    117: [118, 168, 175], # Active Prompting -> APE, Continuous Eval, Human Evals
    118: [113, 166, 177], # APE -> Meta-Prompting, GitHub Actions CI, Verbosity Bias
    119: [136, 139, 200], # Graph of Thoughts -> Plan & Solve, DAG Orchestrator, Multi-Agent Architecture
    120: [145, 146, 194], # Soft Prompts -> LoRA Merging, DoRA, RAG vs Fine-tuning

    # RAG and Vector Databases
    121: [101, 147, 167], # Embedding Dim -> Tokenization, GGUF, Semantic Drift
    122: [127, 188, 194], # Semantic Search -> RRF, RBAC Pre-Filter, RAG vs Fine-tuning
    123: [188, 185, 169], # Metadata Filter -> RBAC Filter, Data Lineage, Enterprise Gateway
    124: [126, 129, 178], # Multi-Rep -> Parent-Doc Retriever, RAPTOR, RAG Evals
    125: [124, 181, 199], # Doc Parsing -> Multi-Rep Retrieval, Indirect Injection, System Design
    126: [124, 152, 178], # Parent-Doc -> Multi-Rep, Prefix Cache, RAG Evals
    127: [122, 178, 199], # RRF -> Semantic Search, RAG Evals, Multi-Tenant System Design
    128: [115, 152, 178], # Compression -> Context Truncation, Prefix Cache, RAG Evals
    129: [119, 124, 199], # RAPTOR -> Graph of Thoughts, Multi-Rep, System Design
    130: [136, 176, 178], # Self-RAG -> Plan-and-Solve, NLI Hallucination, Ragas Evals

    # AI Agents and MCP
    131: [135, 140, 190], # Tool Schema -> Agent System Prompt, Sandbox Security, MCP Audit
    132: [139, 169, 200], # State Machine -> DAG Orchestrator, LLM Gateway, Staff Multi-Agent
    133: [184, 190, 200], # HITL -> Jailbreaking, MCP Audit, Staff Multi-Agent
    134: [138, 154, 163], # Sync vs Async -> MCP Streaming, Connection Pooling, TTFT SLO
    135: [131, 164, 191], # Agent System Prompt -> Tool Schema, SemVer Prompts, Coding Interview
    136: [119, 139, 200], # Plan & Solve -> Graph of Thoughts, DAG Orchestrator, Staff Multi-Agent
    137: [127, 181, 199], # Agentic Search -> RRF, Indirect Injection, System Design
    138: [134, 154, 190], # MCP Streaming -> Async Execution, Connection Pooling, MCP Audit
    139: [132, 136, 200], # DAG Orchestrator -> State Machine, Plan & Solve, Staff Multi-Agent
    140: [131, 190, 200], # Sandbox -> Tool Schema, MCP Audit, Staff Multi-Agent

    # Fine-Tuning and Adaptation
    141: [145, 149, 194], # Instruction Formatting -> LoRA, ORPO, RAG vs Fine-tuning
    142: [103, 143, 150], # LR Scheduling -> Logits, Grad Accumulation, DeepSpeed ZeRO
    143: [142, 144, 150], # Grad Accum -> LR Scheduling, Mixed Precision, DeepSpeed ZeRO
    144: [101, 143, 147], # BF16 -> Tokenization, Grad Accum, GGUF
    145: [120, 146, 194], # Weight Merging -> Soft Prompts, DoRA, RAG vs Fine-tuning
    146: [145, 149, 150], # DoRA -> Weight Merging, ORPO, DeepSpeed ZeRO
    147: [121, 144, 148], # GGUF -> Embedding Dim, Mixed Precision, AWQ
    148: [147, 157, 159], # AWQ -> GGUF, Tensor Parallelism, PagedAttention
    149: [141, 146, 175], # ORPO -> Instruction Formatting, DoRA, Human Evals
    150: [106, 143, 157], # DeepSpeed ZeRO -> MoE, Grad Accum, Tensor Parallelism

    # AI System Design
    151: [153, 154, 169], # Load Balancing -> Router, Connection Pooling, LLM Gateway
    152: [108, 126, 159], # Prefix Cache -> SWA, Parent-Doc, PagedAttention
    153: [116, 151, 169], # LLM Router -> Directional Stimulus, Load Balancing, Gateway
    154: [134, 138, 163], # Connection Pooling -> Async Execution, MCP Streaming, SLO
    155: [165, 169, 196], # Graceful Degradation -> Provider Fallback, Gateway, System Design
    156: [104, 108, 159], # Chunked Prefill -> Attention Mask, SWA, PagedAttention
    157: [106, 150, 196], # Parallelism (TP/PP) -> MoE, DeepSpeed ZeRO, System Design
    158: [107, 159, 196], # Medusa -> Linear Attention, PagedAttention, System Design
    159: [107, 152, 156], # PagedAttention -> Linear Attn, Prefix Cache, Chunked Prefill
    160: [152, 159, 199], # Global Architecture -> Prefix Cache, PagedAttention, Multi-Tenant RAG

    # LLMOps and Production AI
    161: [162, 163, 170], # Logging -> Cost Attribution, SLO Monitoring, Confidential Telemetry
    162: [153, 161, 169], # Cost Attribution -> Router, Logging, LLM Gateway
    163: [134, 154, 161], # SLO Monitoring -> Async Tools, Connection Pooling, Logging
    164: [111, 135, 166], # SemVer Prompts -> Priming, Agent Prompt, CI/CD Evals
    165: [155, 169, 196], # Fallback -> Graceful Degradation, Gateway, System Design
    166: [118, 164, 173], # CI/CD Evals -> APE, SemVer Prompts, Assertion Evals
    167: [121, 168, 178], # Semantic Drift -> Embedding Dim, Continuous Eval, Ragas Evals
    168: [117, 167, 175], # Continuous Eval -> Active Prompting, Semantic Drift, Human Evals
    169: [123, 151, 162], # LLM Gateway -> Metadata Filter, Load Balancing, Cost Attribution
    170: [161, 182, 188], # Confidential Telemetry -> Structured Logging, PII Masking, RBAC

    # Evaluation and Testing
    171: [172, 173, 178], # EM vs F1 -> BLEU/ROUGE, Assertion Evals, Ragas Evals
    172: [171, 176, 178], # BLEU/ROUGE -> EM vs F1, NLI Hallucination, Ragas Evals
    173: [112, 166, 171], # Assertion Evals -> Negative Prompting, CI/CD Evals, EM vs F1
    174: [113, 168, 178], # Synthetic Evals -> Meta-Prompting, Continuous Eval, Ragas Evals
    175: [117, 149, 179], # Human Evals -> Active Prompting, ORPO, Elo Rating
    176: [110, 130, 178], # NLI Hallucination -> Diff Attention, Self-RAG, Ragas Evals
    177: [118, 175, 179], # Verbosity Bias -> APE, Human Evals, Elo Rating
    178: [124, 126, 176], # Ragas Evals -> Multi-Rep, Parent-Doc, NLI Hallucination
    179: [175, 177, 192], # Elo Rating -> Human Evals, Verbosity Bias, AI Portfolio
    180: [181, 184, 197], # Red Teaming -> Indirect Injection, Jailbreaking, Live Coding Debug

    # AI Safety and Governance
    181: [125, 137, 186], # Indirect Injection -> Doc Parsing, Agentic Search, Data Exfiltration
    182: [161, 170, 188], # PII Masking -> Structured Logging, Confidential Telemetry, RBAC
    183: [181, 185, 186], # Copyright -> Indirect Injection, Data Lineage, Data Exfiltration
    184: [112, 133, 187], # Jailbreaking -> Negative Prompting, HITL, Llama Guard
    185: [123, 170, 188], # Data Lineage -> Metadata Filter, Confidential Telemetry, RBAC
    186: [181, 183, 190], # Data Exfiltration -> Indirect Injection, Copyright, MCP Audit
    187: [184, 188, 189], # Llama Guard -> Jailbreaking, RBAC Filter, NeMo Guardrails
    188: [123, 170, 185], # RBAC Filter -> Metadata Filter, Confidential Telemetry, Data Lineage
    189: [132, 139, 187], # NeMo Guardrails -> State Machine, DAG Orchestrator, Llama Guard
    190: [131, 138, 140], # MCP Audit -> Tool Schema, MCP Streaming, Sandbox Security

    # Interview Experience
    191: [111, 135, 197], # SDK vs Frameworks -> Priming, Agent System Prompt, Live Coding Debug
    192: [166, 178, 198], # AI Portfolio -> CI/CD Evals, Ragas Evals, Production Rigor
    193: [191, 194, 198], # Core Roles -> SDK vs Frameworks, RAG vs Fine-tuning, Production Rigor
    194: [120, 122, 141], # RAG vs Fine-tuning -> Soft Prompts, Semantic Search, Instruction Format
    195: [112, 176, 178], # Hallucination Defense -> Negative Prompting, NLI Hallucination, Ragas Evals
    196: [151, 157, 199], # System Design Interview -> Load Balancing, Parallelism, Multi-Tenant RAG
    197: [173, 180, 191], # Live Coding Debug -> Assertion Evals, Red Teaming, SDK vs Frameworks
    198: [166, 192, 193], # Production Rigor -> CI/CD Evals, AI Portfolio, Core Roles
    199: [123, 127, 159], # Multi-Tenant RAG System -> Metadata Filter, RRF, PagedAttention
    200: [119, 136, 139], # Staff Multi-Agent System -> Graph of Thoughts, Plan & Solve, DAG Orchestrator

    # AI Safety and Governance (model-level and regulatory risk)
    201: [91, 185, 202],  # Model Inversion -> System Prompt Exfiltration, Data Lineage, Data Poisoning
    202: [201, 203, 185], # Data Poisoning -> Model Inversion, Model Supply Chain, Data Lineage
    203: [202, 185, 140], # Model Supply Chain -> Data Poisoning, Data Lineage, Sandbox Security
    204: [205, 183, 185], # EU AI Act Tiers -> NIST AI RMF, Copyright, Data Lineage
    205: [204, 93, 201],  # NIST AI RMF -> EU AI Act Tiers, Hallucination, Model Inversion
}


def main():
    topics = load_topics(REPO_ROOT)
    questions = all_questions(topics)
    
    id_to_question = {q.id: q for q in questions}
    
    modified_count = 0
    for q_id, target_ids in CROSS_LINK_MAP.items():
        if q_id not in id_to_question:
            continue
            
        q = id_to_question[q_id]
        
        # Build wikilink list items
        wikilink_items = []
        for tid in target_ids:
            if tid in id_to_question:
                target_q = id_to_question[tid]
                rel_path = f"../{target_q.path.parent.name}/{target_q.filename}"
                # Wikilink format [[Title]] + standard markdown link format
                wikilink_items.append(
                    f"- [[{target_q.title}]] (`#{target_q.id}`): [{target_q.title}]({rel_path})"
                )
                
        if not wikilink_items:
            continue
            
        content = q.path.read_text(encoding="utf-8")
        
        # Check if ## Related Concepts / ## Related Questions section exists
        if "## Related Concepts" in content or "## Related Questions" in content:
            continue
            
        # Insert before the footer rule. Match a `---` that is alone on its line
        # AFTER the frontmatter block: a bare `content.rsplit("---")` would land
        # on the frontmatter's closing delimiter in any file lacking a footer,
        # injecting the section into the header instead of the end.
        _, body = parse_frontmatter(content)
        footer = FOOTER_RULE_RE.search(body)
        related_section = "## Related Concepts\n\n" + "\n".join(wikilink_items) + "\n"
        if footer:
            offset = len(content) - len(body)
            cut = offset + footer.start()
            new_content = content[:cut] + related_section + "\n" + content[cut:]
        else:
            new_content = content.rstrip() + "\n\n" + related_section
            
        q.path.write_text(new_content, encoding="utf-8")
        modified_count += 1
        
    print(f"Successfully injected [[wikilinks]] into {modified_count} question files.")


if __name__ == "__main__":
    main()
