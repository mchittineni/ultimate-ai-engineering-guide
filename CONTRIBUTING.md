# Contributing to Ultimate AI Engineering Guide

Thank you for helping build the ultimate, production-grade guide for AI Engineering interviews!

## 🎯 Content Philosophy

Every question and answer in this repository follows a strict quality standard:

1. **Answer to interviewer depth**: Don't stop at definitions. Explain _why_ it works, trade-offs, edge cases, and production failure modes.
2. **Standardized answer structure**, in this order:
   - `YAML Frontmatter` (title, id, category, difficulty, tags)
   - `# Title` — must match the frontmatter `title` exactly
   - `**Short answer:**` (1-2 sentences you can speak out loud)
   - `## Detail` (Deep explanation, architectural mechanics, or math)
   - `## Example` (Code snippet, architectural flow, or benchmark table)
   - `## Interview tips` (Probing questions, traps, or real-world stories)
   - `## Related Concepts` (cross-topic `[[wikilinks]]` — generated, see below)
   - `---` followed by `[⬅ Back to <Topic>](./README.md) · [All topics](../README.md)`
3. **Working code**: every code example should actually run and produce the output its comments claim. If a snippet is illustrative rather than production-ready, say so in the surrounding prose.

## 📛 File Naming: the slug must match the title

This is the rule contributors trip over most. The filename is **not** a free-form kebab-case summary — it must be the title, slugified:

```text
title: "What is KV Cache and how does it speed up inference?"
file:   what-is-kv-cache-and-how-does-it-speed-up-inference.md
```

Slugification lowercases the title, expands `&` to `and`, **drops apostrophes** (`can't` → `cant`), and replaces every other run of non-alphanumeric characters with a single `-`. `validate_content.py` computes the expected slug and fails on any mismatch, so rename the file rather than guessing.

## 📝 Frontmatter Format

```yaml
---
title: "What is KV Cache and how does it speed up inference?"
id: 206
category: "LLM Fundamentals"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - llm-fundamentals
  - interview-questions
---
```

Rules enforced by the validator:

- `id` — unique across the whole repository. Take the next number after the current maximum.
- `category` — must match the topic's display title exactly (e.g. `"LLM Fundamentals"`, not the directory name).
- `difficulty` — exactly one of `Beginner`, `Intermediate`, `Advanced`.
- `tags` — must include `ai-engineering` and `interview-questions`; the topic slug tag is conventional.

## 🛠️ Local Setup & Validation

No dependencies to install — every script is stdlib-only Python 3.

```bash
# 1. Validate frontmatter, naming, IDs, links, and index freshness
python3 scripts/validate_content.py

# 2. Regenerate topic indexes and root README stats/TOC
python3 scripts/generate_indexes.py

# 3. Add cross-topic [[wikilinks]] to any question missing them
python3 scripts/inject_wikilinks.py

# 4. Rebuild the published 3D knowledge graph (docs/index.html)
python3 scripts/build_knowledge_graph.py
```

`generate_indexes.py --check` reports drift without writing, which is what CI runs.

> **Indexes are generated, never hand-edited.** Topic `README.md` files and the root README's `TOC`/`STATS` blocks are produced from the question files themselves. Editing them by hand is always the wrong move — your change will be overwritten and CI will flag the drift.

## 🚀 Creating a New Question

1. Locate or create the appropriate topic directory registered in `scripts/topic_meta.json`.
2. Name the file to match the slugified title (see above).
3. Pick the next available unique `id`.
4. Write the answer following the standard structure.
5. Run `python3 scripts/validate_content.py` and fix anything it reports.
6. Run `python3 scripts/generate_indexes.py` to add your question to the indexes.
7. Run `python3 scripts/inject_wikilinks.py` and `python3 scripts/build_knowledge_graph.py`.
8. Commit the question **and** the regenerated indexes and graph together.

### Adding a new topic

Register the directory in `scripts/topic_meta.json` with an `order`, `group`, `description`, and `study_notes`. An unregistered directory containing markdown is a validation error, which is deliberate — it catches content that would otherwise never appear in any index.

## ✅ Things the validator will reject

- A filename whose slug does not match the title.
- A duplicate or missing `id`, or a `category` that does not match the topic.
- A `# heading` that differs from the frontmatter `title`.
- A missing required tag, or a difficulty outside the three allowed values.
- A broken relative link (links inside code fences are ignored).
- Four-space-indented prose, which silently renders as a code block.
- Stale indexes — regenerate them before committing.
