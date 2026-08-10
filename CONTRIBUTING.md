# Contributing to Ultimate AI Engineering Guide

Thank you for helping build the ultimate, production-grade guide for AI Engineering interviews!

## 🎯 Content Philosophy

Every question and answer in this repository follows a strict quality standard:

1. **Answer to interviewer depth**: Don't stop at definitions. Explain _why_ it works, trade-offs, edge cases, and production failure modes.
2. **Standardized answer structure**:
   - `YAML Frontmatter` (title, id, category, difficulty, tags)
   - `# Title`
   - `**Short answer:**` (1-2 sentences you can speak out loud)
   - `## Detail` (Deep explanation, architectural mechanics, or math)
   - `## Example` (Code snippet, architectural flow, or benchmark table)
   - `## Interview tips` (Probing questions, traps, or real-world stories)
   - `[⬅ Back to <Topic>](./README.md) · [All topics](../README.md)`

## 🛠️ Local Setup & Validation

Before submitting a Pull Request, run the validation tools locally:

```bash
# 1. Validate frontmatter, links, question IDs, and structure
python3 scripts/validate_content.py

# 2. Automatically regenerate topic indexes and main README stats
python3 scripts/generate_indexes.py
```text

## 📝 Frontmatter Format

```yaml
---
title: "What is KV Cache in LLMs?"
id: 101
category: "LLM Fundamentals"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - llm-fundamentals
  - interview-questions
---
```text

## 🚀 Creating a New Question

1. Locate or create the appropriate topic directory registered in `scripts/topic_meta.json`.
2. Name the file using kebab-case: `what-is-kv-cache.md`.
3. Pick the next available unique `id`.
4. Run `python3 scripts/generate_indexes.py` to add your question to the indexes.
5. Run `python3 scripts/validate_content.py` to ensure everything passes cleanly.
