#!/usr/bin/env python3
"""Generate an interactive HTML knowledge graph for GitHub Pages.

Parses all Markdown questions and topic indexes, extracts connections (categories,
shared tags, and explicit cross-file relative links), and builds an interactive 3D/2D
Force Graph using Force-Graph for GitHub Pages static site deployment.

Usage:
    python3 scripts/build_knowledge_graph.py [--output docs/index.html]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Add scripts dir to sys.path
SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))

from lib_content import REPO_ROOT, all_questions, load_topics, topic_meta

LINK_RE = re.compile(r"\[[^\]]*\]\(([^:)\s][^)\s]*)\)")
WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")

DIFFICULTY_COLORS = {
    "Beginner": "#10b981",      # Emerald Green
    "Intermediate": "#f59e0b",  # Amber Yellow
    "Advanced": "#ef4444",      # Rose Red
    "Topic": "#06b6d4",         # Cyan / Terminal Teal
}

# Keys MUST match the `group` values in scripts/topic_meta.json (and the
# GROUP_ORDER list in generate_indexes.py). A group missing here silently falls
# back to the default cyan, which makes every topic hub the same colour and
# quietly destroys the section encoding.
GROUP_COLORS = {
    "Foundations & Models": "#3b82f6",        # Blue
    "Retrieval & Agentic Systems": "#8b5cf6",  # Violet
    "Adaptation & System Design": "#f59e0b",   # Amber
    "Operations & Quality": "#10b981",         # Emerald
    "Governance & Career Track": "#ef4444",    # Rose
}


def extract_internal_links(file_path: Path, text: str, title_to_path_map: dict | None = None) -> list[Path]:
    """Extract relative markdown links and [[wikilinks]] targeting other question files."""
    linked_paths = []
    # 1. Standard relative markdown links
    for match in LINK_RE.findall(text):
        target = match.split("#", 1)[0]
        if not target or not target.endswith(".md"):
            continue
        resolved = (file_path.parent / target).resolve()
        if resolved.exists() and resolved != file_path:
            linked_paths.append(resolved)

    # 2. Obsidian / Wiki style [[wikilinks]]
    if title_to_path_map:
        for match in WIKILINK_RE.findall(text):
            target_name = match.strip().lower()
            if target_name in title_to_path_map:
                resolved = title_to_path_map[target_name]
                if resolved != file_path:
                    linked_paths.append(resolved)

    return linked_paths


def build_graph_data(repo_root: Path = REPO_ROOT) -> dict:
    topics = load_topics(repo_root)
    questions = all_questions(topics)
    meta = topic_meta()

    nodes = []
    edges = []
    edge_set = set()

    # 1. Add Topic Nodes
    for t in topics:
        t_group = meta.get(t.directory, {}).get("group", "Other")
        nodes.append({
            "id": f"topic:{t.directory}",
            "label": t.title,
            "group": "Topic Hub",
            "section": t_group,
            "val": 16,
            "color": GROUP_COLORS.get(t_group, DIFFICULTY_COLORS["Topic"]),
            "url": f"./{t.directory}/README.md",
            "category": t.title,
            "type": "topic"
        })

    # Path to Node ID map and Title to Path map
    path_to_id = {q.path.resolve(): f"q:{q.id}" for q in questions}
    title_to_path_map = {q.title.strip().lower(): q.path.resolve() for q in questions}
    for q in questions:
        title_to_path_map[f"q{q.id}"] = q.path.resolve()
        title_to_path_map[f"question {q.id}"] = q.path.resolve()
        title_to_path_map[f"#{q.id}"] = q.path.resolve()

    # 2. Add Question Nodes and Topic-to-Question Edges
    for q in questions:
        node_id = f"q:{q.id}"
        topic_dir = q.path.parent.name
        topic_node_id = f"topic:{topic_dir}"
        t_group = meta.get(topic_dir, {}).get("group", "Other")

        nodes.append({
            "id": node_id,
            "label": f"#{q.id} {q.title}",
            "title": q.title,
            "group": q.difficulty,
            "section": t_group,
            "val": 6 if q.difficulty == "Advanced" else (4 if q.difficulty == "Intermediate" else 3),
            "color": DIFFICULTY_COLORS.get(q.difficulty, "#3b82f6"),
            "url": f"./{q.path.relative_to(repo_root)}",
            "category": q.category,
            "difficulty": q.difficulty,
            "tags": q.tags,
            "type": "question"
        })

        # Connect Question to its Topic Node
        edge_key = (topic_node_id, node_id, "topic")
        if edge_key not in edge_set:
            edge_set.add(edge_key)
            edges.append({
                "source": topic_node_id,
                "target": node_id,
                "type": "topic-link",
                "color": "rgba(6, 182, 212, 0.4)"
            })

        # 3. Extract Explicit Markdown Links and [[wikilinks]] between Questions
        for linked_path in extract_internal_links(q.path, q.body, title_to_path_map):
            if linked_path in path_to_id:
                target_id = path_to_id[linked_path]
                e_key = (node_id, target_id, "cross-link")
                if e_key not in edge_set and (target_id, node_id, "cross-link") not in edge_set:
                    edge_set.add(e_key)
                    edges.append({
                        "source": node_id,
                        "target": target_id,
                        "type": "cross-link",
                        "color": "rgba(59, 130, 246, 0.6)"
                    })

    # 4. Connect Questions sharing identical specific tags (Tag Similarity Edges)
    tag_map: dict[str, list[str]] = {}
    for q in questions:
        for tag in q.tags:
            if tag in {"ai-engineering", "interview-questions", "index"}:
                continue # Skip generic tags
            tag_map.setdefault(tag, []).append(f"q:{q.id}")

    for tag, q_ids in tag_map.items():
        if len(q_ids) > 1 and len(q_ids) <= 6:
            for i in range(len(q_ids)):
                for j in range(i + 1, len(q_ids)):
                    src, tgt = q_ids[i], q_ids[j]
                    e_key = (src, tgt, f"tag:{tag}")
                    if e_key not in edge_set and (tgt, src, f"tag:{tag}") not in edge_set:
                        edge_set.add(e_key)
                        edges.append({
                            "source": src,
                            "target": tgt,
                            "type": "tag-link",
                            "color": "rgba(245, 158, 11, 0.2)"
                        })

    return {"nodes": nodes, "links": edges}


REPO_BLOB = "https://github.com/mchittineni/ultimate-ai-engineering-guide/blob/main/"


def flatten(graph: dict) -> dict:
    """Reshape the node/link graph into the flat form the Weave view renders.

    The view needs each question once, with its topic, section, difficulty and
    the ids it cross-links to -- plus the topic order the repo itself defines,
    which is what puts related topics beside each other on the rim.
    """
    nodes, links = graph["nodes"], graph["links"]

    topics = {
        n["category"]: {
            "section": n.get("section", ""),
            "color": n.get("color", "#888888"),
            "url": n["url"],
        }
        for n in nodes if n["type"] == "topic"
    }

    neighbours: dict[str, set[str]] = {n["id"]: set() for n in nodes}
    for link in links:
        if link["type"] == "cross-link":
            neighbours[link["source"]].add(link["target"])
            neighbours[link["target"]].add(link["source"])

    questions = [
        {
            "id": n["id"],
            "num": int(n["id"].split(":")[1]),
            "title": n.get("title") or n["label"],
            "topic": n["category"],
            "section": n.get("section", ""),
            "difficulty": n.get("difficulty", ""),
            "color": n.get("color", "#888888"),
            "url": n["url"],
            "tags": [t for t in n.get("tags", []) if t not in {"ai-engineering", "interview-questions"}],
            "links": sorted(neighbours[n["id"]]),
        }
        for n in nodes if n["type"] == "question"
    ]
    questions.sort(key=lambda q: q["num"])

    topic_order = [n["category"] for n in nodes if n["type"] == "topic"]
    section_order: list[str] = []
    for n in nodes:
        if n["type"] == "topic" and n.get("section") and n["section"] not in section_order:
            section_order.append(n["section"])

    cross_links = sum(1 for l in links if l["type"] == "cross-link")

    return {
        "questions": questions,
        "topics": topics,
        "topicOrder": topic_order,
        "sectionOrder": section_order,
        "crossLinks": cross_links,
        "repoBlob": REPO_BLOB,
    }


# Placeholder substitution rather than str-formatting: the template is a large
# body of CSS and JS whose every literal brace would otherwise need doubling,
# which has silently broken this file before.
HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Engineering Knowledge Graph</title>
<script>
  (function () {
    var mode;
    try { mode = localStorage.getItem('ai-eng-graph-theme'); } catch (e) { /* private mode */ }
    if (mode !== 'light' && mode !== 'dark' && mode !== 'system') mode = 'system';
    var effective = mode === 'system'
      ? (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
      : mode;
    document.documentElement.setAttribute('data-theme-mode', mode);
    document.documentElement.setAttribute('data-theme', effective);
  })();
</script>
<style>
/* ---------------------------------------------------------------------------
   Tokens. The bare :root carries the complete LIGHT palette. Dark is redefined
   twice: behind prefers-color-scheme (guarded so an explicit light choice still
   wins) and behind [data-theme="dark"] so the toggle wins too. Components read
   tokens only -- a colour defined only inside a theme block would vanish in the
   un-stamped state, which is the classic unreadable-page bug.
   --------------------------------------------------------------------------- */
:root {
  --ground: #edf1f5;
  --surface: #ffffff;
  --surface-2: #e4ebf1;
  --ink: #0f1620;
  --ink-soft: #43535f;
  --ink-faint: #6b7c8a;
  --rule: #cbd6df;
  --rule-soft: #dde5ec;
  --accent: #1f5c8b;
  --accent-ink: #17486d;
  --accent-wash: rgba(31, 92, 139, 0.10);
  --wire: rgba(23, 37, 51, 0.13);
  --wire-hot: rgba(23, 72, 109, 0.85);
  --shadow: 0 18px 40px -24px rgba(15, 22, 32, 0.45);
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --ground: #0e141b;
    --surface: #151d26;
    --surface-2: #1c2733;
    --ink: #e6edf4;
    --ink-soft: #a7b6c4;
    --ink-faint: #7c8d9c;
    --rule: #2a3744;
    --rule-soft: #212c38;
    --accent: #58a6d8;
    --accent-ink: #8cc6ec;
    --accent-wash: rgba(88, 166, 216, 0.14);
    --wire: rgba(167, 182, 196, 0.18);
    --wire-hot: rgba(140, 198, 236, 0.9);
    --shadow: 0 18px 40px -24px rgba(0, 0, 0, 0.8);
  }
}
:root[data-theme="dark"] {
  --ground: #0e141b;
  --surface: #151d26;
  --surface-2: #1c2733;
  --ink: #e6edf4;
  --ink-soft: #a7b6c4;
  --ink-faint: #7c8d9c;
  --rule: #2a3744;
  --rule-soft: #212c38;
  --accent: #58a6d8;
  --accent-ink: #8cc6ec;
  --accent-wash: rgba(88, 166, 216, 0.14);
  --wire: rgba(167, 182, 196, 0.18);
  --wire-hot: rgba(140, 198, 236, 0.9);
  --shadow: 0 18px 40px -24px rgba(0, 0, 0, 0.8);
}

*, *::before, *::after { box-sizing: border-box; }
html, body { height: 100%; }

body {
  margin: 0;
  background: var(--ground);
  color: var(--ink);
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  font-size: 15px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  overflow: hidden;
}

.mono { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; }

.label {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 10px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--ink-faint);
}

:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; border-radius: 3px; }

#shell { display: flex; flex-direction: column; height: 100vh; }

/* --------------------------------- Header -------------------------------- */
header {
  flex: none;
  background: var(--surface);
  border-bottom: 1px solid var(--rule);
  padding: 12px 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.masthead { display: flex; align-items: baseline; gap: 14px; flex-wrap: wrap; }

h1 {
  margin: 0;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.06em;
}

.masthead .stats { color: var(--ink-faint); font-size: 12.5px; font-variant-numeric: tabular-nums; }

#theme-switch { margin-left: auto; display: flex; gap: 2px; }

.theme-btn {
  appearance: none;
  background: transparent;
  border: 1px solid var(--rule);
  color: var(--ink-soft);
  font: inherit;
  font-size: 12px;
  line-height: 1;
  padding: 5px 9px;
  cursor: pointer;
}
.theme-btn:first-child { border-radius: 999px 0 0 999px; }
.theme-btn:last-child { border-radius: 0 999px 999px 0; }
.theme-btn + .theme-btn { border-left: 0; }
.theme-btn:hover { background: var(--surface-2); }
.theme-btn[aria-checked="true"] { background: var(--accent-wash); border-color: var(--accent); color: var(--ink); }

.controls { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }

#search {
  flex: 0 1 260px;
  min-width: 180px;
  font: inherit;
  font-size: 13px;
  color: var(--ink);
  background: var(--ground);
  border: 1px solid var(--rule);
  border-radius: 6px;
  padding: 6px 11px;
}
#search::placeholder { color: var(--ink-faint); }

.chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font: inherit;
  font-size: 11.5px;
  color: var(--ink-soft);
  background: var(--ground);
  border: 1px solid var(--rule);
  border-radius: 999px;
  padding: 5px 11px;
  cursor: pointer;
  white-space: nowrap;
}
.chip:hover { background: var(--surface-2); }
.chip[aria-pressed="false"] { opacity: 0.42; }
.chip[aria-pressed="true"] { border-color: var(--accent); color: var(--ink); }
.chip .dot { width: 8px; height: 8px; border-radius: 50%; flex: none; }
.chip .ct { font-family: ui-monospace, Menlo, monospace; font-variant-numeric: tabular-nums; color: var(--ink-faint); }

#reset {
  font: inherit;
  font-size: 10px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  background: none;
  border: 0;
  color: var(--accent-ink);
  cursor: pointer;
  padding: 5px 4px;
}

#match { font-size: 11.5px; color: var(--ink-faint); font-variant-numeric: tabular-nums; margin-left: auto; }

/* --------------------------------- Stage --------------------------------- */
#stage { flex: 1; display: grid; grid-template-columns: 1fr 300px; min-height: 0; }

#canvas-wrap { position: relative; min-width: 0; overflow: hidden; }
svg { display: block; width: 100%; height: 100%; touch-action: none; }
#scene { cursor: grab; }
#scene.dragging { cursor: grabbing; }

.node { cursor: pointer; }

#hint {
  position: absolute;
  left: 16px;
  bottom: 14px;
  pointer-events: none;
}

#zoom {
  position: absolute;
  right: 14px;
  bottom: 14px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.zoom-btn {
  width: 30px;
  height: 30px;
  font: inherit;
  font-size: 15px;
  line-height: 1;
  color: var(--ink-soft);
  background: var(--surface);
  border: 1px solid var(--rule);
  border-radius: 6px;
  cursor: pointer;
}
.zoom-btn:hover { background: var(--surface-2); }

/* -------------------------------- Detail --------------------------------- */
#detail {
  border-left: 1px solid var(--rule);
  background: var(--surface);
  padding: 16px;
  overflow-y: auto;
  min-height: 0;
}
#detail .empty-state { color: var(--ink-faint); font-size: 13px; }
#detail h2 { margin: 8px 0 10px; font-size: 15px; line-height: 1.3; text-wrap: balance; }

.pill {
  display: inline-flex;
  font-family: ui-monospace, Menlo, monospace;
  font-size: 9.5px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  border: 1px solid currentColor;
  border-radius: 999px;
  padding: 3px 8px;
}

.meta { display: grid; grid-template-columns: auto 1fr; gap: 3px 10px; margin: 0 0 14px; font-size: 12.5px; }
.meta dt {
  color: var(--ink-faint);
  font-family: ui-monospace, Menlo, monospace;
  font-size: 9.5px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  align-self: center;
}
.meta dd { margin: 0; }

.conn { border-top: 1px solid var(--rule-soft); padding-top: 10px; }
.conn ul { list-style: none; margin: 6px 0 0; padding: 0; display: grid; gap: 2px; }
.conn button {
  font: inherit;
  font-size: 12px;
  line-height: 1.3;
  text-align: left;
  width: 100%;
  color: var(--accent-ink);
  background: none;
  border: 0;
  border-radius: 4px;
  padding: 3px 5px;
  cursor: pointer;
}
.conn button:hover { background: var(--accent-wash); }

.source-link { display: inline-block; margin-top: 14px; font-size: 12px; color: var(--accent-ink); }

#results { list-style: none; margin: 0; padding: 0; display: grid; gap: 2px; }
#results button {
  font: inherit;
  font-size: 12px;
  text-align: left;
  width: 100%;
  color: var(--ink-soft);
  background: none;
  border: 0;
  border-radius: 4px;
  padding: 4px 6px;
  cursor: pointer;
}
#results button:hover { background: var(--surface-2); color: var(--ink); }

@media (max-width: 900px) {
  #stage { grid-template-columns: 1fr; }
  #detail { position: absolute; inset: auto 0 0 0; max-height: 52%; border-top: 1px solid var(--rule); border-left: 0; display: none; }
  #detail.open { display: block; }
}

@media (prefers-reduced-motion: reduce) {
  * { transition: none !important; }
}
</style>
</head>
<body>
<div id="shell">
  <header>
    <div class="masthead">
      <h1>AI ENGINEERING KNOWLEDGE GRAPH</h1>
      <span class="stats">__QUESTION_COUNT__ questions · __TOPIC_COUNT__ topics · __LINK_COUNT__ cross-links</span>
      <div id="theme-switch" role="radiogroup" aria-label="Colour theme">
        <button type="button" class="theme-btn" role="radio" aria-checked="false" data-theme-choice="light" title="Light">☀</button>
        <button type="button" class="theme-btn" role="radio" aria-checked="false" data-theme-choice="dark" title="Dark">☾</button>
        <button type="button" class="theme-btn" role="radio" aria-checked="false" data-theme-choice="system" title="Match system">◐</button>
      </div>
    </div>
    <div class="controls">
      <input type="search" id="search" placeholder="Search questions…" aria-label="Search questions">
      <div id="section-chips" style="display:flex;gap:6px;flex-wrap:wrap" role="group" aria-label="Filter by section"></div>
      <div id="difficulty-chips" style="display:flex;gap:6px;flex-wrap:wrap" role="group" aria-label="Filter by difficulty"></div>
      <button type="button" id="reset">Reset</button>
      <span id="match" role="status" aria-live="polite"></span>
    </div>
  </header>

  <div id="stage">
    <div id="canvas-wrap">
      <svg id="graph" role="img" aria-label="Circular knowledge graph: questions grouped by topic, cross-links drawn as bundled curves"></svg>
      <p id="hint" class="label">Drag to pan · scroll to zoom · / to search</p>
      <div id="zoom" role="group" aria-label="Zoom">
        <button type="button" class="zoom-btn" id="zoom-in" aria-label="Zoom in">+</button>
        <button type="button" class="zoom-btn" id="zoom-out" aria-label="Zoom out">−</button>
        <button type="button" class="zoom-btn" id="zoom-reset" aria-label="Reset view" title="Reset view">⤾</button>
      </div>
    </div>
    <aside id="detail" aria-live="polite">
      <p class="empty-state">Select a question on the rim to see its topic, difficulty and cross-links.</p>
    </aside>
  </div>
</div>

<script>
const DATA = __DATA__;
const Q = DATA.questions;
const BY_ID = new Map(Q.map(q => [q.id, q]));
const TAU = Math.PI * 2;
const REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;
const SVG_NS = 'http://www.w3.org/2000/svg';

/* The data's colours were chosen against a dark ground. On a light ground some
   of them fall under the 3:1 floor WCAG 1.4.11 sets for non-text graphics --
   amber at 1.89:1, emerald at 2.23:1 -- and read as washed out.

   Darkening the whole palette to fix those two turns the page muddy, so this
   adjusts each colour only as far as it needs to go: anything already clearing
   the floor is left exactly as-is, and the rest are mixed toward the ink in
   small steps until they just clear it. Blue, violet and rose come through
   untouched; only amber and emerald move. */
const INK_RGB = [15, 22, 32];
const LIGHT_GROUND = [237, 241, 245];
const MIN_CONTRAST = 3.2;
const toneCache = new Map();

const isLight = () => document.documentElement.getAttribute('data-theme') !== 'dark';

const channel = c => {
  const v = c / 255;
  return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
};
const luminance = rgb => 0.2126 * channel(rgb[0]) + 0.7152 * channel(rgb[1]) + 0.0722 * channel(rgb[2]);

function contrast(a, b) {
  const la = luminance(a), lb = luminance(b);
  return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05);
}

function tone(hex) {
  if (!isLight()) return hex;
  if (toneCache.has(hex)) return toneCache.get(hex);

  const h = hex.replace('#', '');
  const rgb = [0, 2, 4].map(i => parseInt(h.slice(i, i + 2), 16));

  let out = hex;
  if (contrast(rgb, LIGHT_GROUND) < MIN_CONTRAST) {
    for (let mix = 0.05; mix <= 0.6; mix += 0.05) {
      const shifted = rgb.map((c, i) => Math.round(c + (INK_RGB[i] - c) * mix));
      if (contrast(shifted, LIGHT_GROUND) >= MIN_CONTRAST) {
        out = '#' + shifted.map(v => v.toString(16).padStart(2, '0')).join('');
        break;
      }
    }
  }
  toneCache.set(hex, out);
  return out;
}

const el = (name, attrs) => {
  const node = document.createElementNS(SVG_NS, name);
  for (const k in attrs) node.setAttribute(k, attrs[k]);
  return node;
};

/* Rim order is the repo's own reading order: topics in registered sequence,
   questions by id within each. Neighbouring topics therefore sit together,
   which is what lets the bundled curves read as topic-to-topic traffic. */
const ORDER = [];
for (const topic of DATA.topicOrder) {
  for (const q of Q) if (q.topic === topic) ORDER.push(q);
}

const SECTIONS = DATA.sectionOrder;
const LEVELS = ['Beginner', 'Intermediate', 'Advanced'].filter(l => Q.some(q => q.difficulty === l));
const SECTION_COLOR = new Map();
for (const t of DATA.topicOrder) {
  const meta = DATA.topics[t];
  if (meta && !SECTION_COLOR.has(meta.section)) SECTION_COLOR.set(meta.section, meta.color);
}
const LEVEL_COLOR = new Map(LEVELS.map(l => [l, (Q.find(q => q.difficulty === l) || {}).color]));

const activeSections = new Set(SECTIONS);
const activeLevels = new Set(LEVELS);
let query = '';
let selected = null;

/* ------------------------------- Filtering ------------------------------- */
function inScope(q) {
  if (!activeSections.has(q.section)) return false;
  if (!activeLevels.has(q.difficulty)) return false;
  if (query) {
    const hay = (q.title + ' ' + q.topic + ' ' + q.section + ' ' + q.difficulty + ' ' + q.tags.join(' ')).toLowerCase();
    if (!hay.includes(query)) return false;
  }
  return true;
}
const wideOpen = () => activeSections.size === SECTIONS.length && activeLevels.size === LEVELS.length && !query;

/* -------------------------------- Chips ---------------------------------- */
function chip(label, count, color, onToggle) {
  const b = document.createElement('button');
  b.type = 'button';
  b.className = 'chip';
  b.setAttribute('aria-pressed', 'true');
  if (color) {
    const dot = document.createElement('span');
    dot.className = 'dot';
    dot.dataset.baseColor = color;
    dot.style.background = tone(color);
    b.appendChild(dot);
  }
  b.appendChild(document.createTextNode(label));
  const ct = document.createElement('span');
  ct.className = 'ct';
  ct.textContent = count;
  b.appendChild(ct);
  b.addEventListener('click', () => {
    const next = b.getAttribute('aria-pressed') !== 'true';
    b.setAttribute('aria-pressed', String(next));
    onToggle(next);
    paint();
  });
  return b;
}

const sectionChips = document.getElementById('section-chips');
for (const s of SECTIONS) {
  sectionChips.appendChild(chip(s, Q.filter(q => q.section === s).length, SECTION_COLOR.get(s), on => {
    on ? activeSections.add(s) : activeSections.delete(s);
  }));
}
const levelChips = document.getElementById('difficulty-chips');
for (const l of LEVELS) {
  levelChips.appendChild(chip(l, Q.filter(q => q.difficulty === l).length, LEVEL_COLOR.get(l), on => {
    on ? activeLevels.add(l) : activeLevels.delete(l);
  }));
}

/* ------------------------------- The weave -------------------------------- */
const svg = document.getElementById('graph');
let scene = null;
let dots = [];
let wires = [];
let bands = [];
let glowBlur = null;
let angleOf = new Map();

function build() {
  const box = svg.getBoundingClientRect();
  const w = Math.max(320, box.width), h = Math.max(320, box.height);
  const cx = w / 2, cy = h / 2;
  const R = Math.max(90, Math.min(w, h) / 2 - 104);

  svg.setAttribute('viewBox', `0 0 ${w} ${h}`);
  svg.replaceChildren();
  dots = []; wires = []; bands = []; angleOf = new Map();

  const defs = el('defs', {});
  const glow = el('filter', { id: 'glow', x: '-30%', y: '-30%', width: '160%', height: '160%' });
  glowBlur = el('feGaussianBlur', { stdDeviation: isLight() ? '1.1' : '2.2', result: 'b' });
  glow.appendChild(glowBlur);
  const merge = el('feMerge', {});
  merge.appendChild(el('feMergeNode', { in: 'b' }));
  merge.appendChild(el('feMergeNode', { in: 'SourceGraphic' }));
  glow.appendChild(merge);
  defs.appendChild(glow);
  svg.appendChild(defs);

  scene = el('g', { id: 'scene' });
  svg.appendChild(scene);

  const wireLayer = el('g', {});
  const pulseLayer = el('g', { filter: 'url(#glow)' });
  const rimLayer = el('g', {});
  scene.append(wireLayer, pulseLayer, rimLayer);

  // Place every question on the rim, grouped by topic with a gap between groups.
  const gap = 0.05;
  const usable = TAU - gap * DATA.topicOrder.length;
  let a = -Math.PI / 2;
  for (const topic of DATA.topicOrder) {
    const qs = ORDER.filter(q => q.topic === topic);
    const sweep = (qs.length / Q.length) * usable;
    const step = sweep / qs.length;
    qs.forEach((q, i) => angleOf.set(q.id, a + step * (i + 0.5)));

    // Topic band + label, flipped on the left half so text never reads upside down.
    const mid = a + sweep / 2;
    const large = sweep > Math.PI ? 1 : 0;
    const p = (r, ang) => [cx + r * Math.cos(ang), cy + r * Math.sin(ang)];
    const [ax, ay] = p(R + 10, a), [bx, by] = p(R + 10, a + sweep);
    const band = el('path', {
      d: `M${ax} ${ay}A${R + 10} ${R + 10} 0 ${large} 1 ${bx} ${by}`,
      fill: 'none', stroke: tone(DATA.topics[topic].color), 'stroke-width': '4', 'stroke-linecap': 'round'
    });
    rimLayer.appendChild(band);
    bands.push({ band, topic });

    const lr = R + 26;
    const [lx, ly] = p(lr, mid);
    const flip = Math.cos(mid) < 0;
    const label = el('text', {
      x: lx, y: ly,
      'text-anchor': flip ? 'end' : 'start',
      'dominant-baseline': 'central',
      transform: `rotate(${(mid * 180 / Math.PI) + (flip ? 180 : 0)} ${lx} ${ly})`,
      fill: 'var(--ink-soft)', 'font-size': '9.5',
      'font-family': 'ui-monospace, Menlo, monospace', 'letter-spacing': '0.07em'
    });
    label.textContent = topic;
    rimLayer.appendChild(label);

    a += sweep + gap;
  }

  const pt = (ang, r) => [cx + r * Math.cos(ang), cy + r * Math.sin(ang)];

  // One curve per unique cross-link, control points pulled toward the centre so
  // links sharing endpoints fall into a common bundle.
  const seen = new Set();
  for (const q of ORDER) {
    for (const id of q.links) {
      const key = q.id < id ? q.id + '|' + id : id + '|' + q.id;
      if (seen.has(key)) continue;
      seen.add(key);
      const a0 = angleOf.get(q.id), a1 = angleOf.get(id);
      if (a0 === undefined || a1 === undefined) continue;
      const [x0, y0] = pt(a0, R), [x1, y1] = pt(a1, R);
      const [c0x, c0y] = pt(a0, R * 0.28), [c1x, c1y] = pt(a1, R * 0.28);
      const d = `M${x0} ${y0}C${c0x} ${c0y} ${c1x} ${c1y} ${x1} ${y1}`;

      const wire = el('path', { d, fill: 'none', stroke: 'var(--wire)', 'stroke-width': '0.9' });
      wireLayer.appendChild(wire);

      const pulse = el('path', {
        d, fill: 'none', stroke: tone(DATA.topics[q.topic].color),
        'stroke-width': '2.2', 'stroke-linecap': 'round'
      });
      pulseLayer.appendChild(pulse);

      wires.push({ wire, pulse, anim: null, a: q.id, b: id });
    }
  }

  // Lengths are only measurable once the paths are in the document.
  const BEAD = 7;
  for (const link of wires) {
    const len = link.pulse.getTotalLength();
    link.pulse.setAttribute('stroke-dasharray', `${BEAD} ${len}`);
    if (REDUCED) {
      link.pulse.setAttribute('stroke-dashoffset', len / 2);
      continue;
    }
    // Negative delay puts every bead mid-flight on frame one, so the field is
    // already scattered instead of firing as a single volley.
    const dur = 3600 + Math.random() * 3200;
    link.anim = link.pulse.animate(
      [{ strokeDashoffset: len + BEAD }, { strokeDashoffset: 0 }],
      { duration: dur, delay: -Math.random() * dur, iterations: Infinity, easing: 'linear' }
    );
  }

  for (const q of ORDER) {
    const [x, y] = pt(angleOf.get(q.id), R);
    const dot = el('circle', {
      cx: x, cy: y, r: 3.4, fill: tone(q.color), class: 'node',
      tabindex: '0', role: 'button', 'aria-label': `#${q.num} ${q.title}`
    });
    dot.addEventListener('click', () => select(q));
    dot.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); select(q); }
    });
    dot.addEventListener('mouseenter', () => hover(q));
    dot.addEventListener('mouseleave', () => hover(null));
    rimLayer.appendChild(dot);
    dots.push({ q, dot });
  }

  applyTransform();
  paint();
}

/* --------------------------------- Paint --------------------------------- */
let hovered = null;
function hover(q) { hovered = q; paint(); }

function paint() {
  const focus = hovered || selected;
  const focusId = focus && focus.id;
  const related = focus ? new Set(focus.links) : null;

  for (const { q, dot } of dots) {
    const scoped = inScope(q);
    const lit = focus ? (q.id === focusId || related.has(q.id)) : scoped;
    dot.setAttribute('opacity', scoped ? (lit ? '1' : '0.22') : '0.07');
    dot.setAttribute('r', q.id === focusId ? '6' : '3.4');
  }

  for (const { wire, pulse, anim, a, b } of wires) {
    const qa = BY_ID.get(a), qb = BY_ID.get(b);
    const scoped = inScope(qa) && inScope(qb);
    const hot = focus ? (a === focusId || b === focusId) : false;

    wire.setAttribute('stroke', hot ? 'var(--wire-hot)' : 'var(--wire)');
    wire.setAttribute('stroke-width', hot ? '1.8' : '0.9');
    wire.setAttribute('opacity', !scoped ? '0.04' : (focus && !hot ? '0.10' : '1'));

    pulse.setAttribute('opacity', !scoped ? '0' : (focus ? (hot ? '1' : '0.05') : '0.85'));
    pulse.setAttribute('stroke-width', hot ? '3' : '2.2');
    // Focused traffic runs hot; the rest keeps drifting so the diagram stays
    // alive rather than freezing around the selection.
    if (anim) anim.playbackRate = hot ? 2.4 : 1;
  }

  const shown = Q.filter(inScope).length;
  document.getElementById('match').textContent =
    wideOpen() ? `All ${Q.length} questions` : `${shown} of ${Q.length} questions`;
}

/* --------------------------------- Detail -------------------------------- */
const detail = document.getElementById('detail');

function select(q) {
  selected = q;
  detail.replaceChildren();
  detail.classList.add('open');

  const pill = document.createElement('span');
  pill.className = 'pill';
  pill.style.color = tone(q.color);
  pill.textContent = q.difficulty || 'QUESTION';
  detail.appendChild(pill);

  const h = document.createElement('h2');
  h.textContent = q.title;
  detail.appendChild(h);

  const dl = document.createElement('dl');
  dl.className = 'meta';
  const rows = [['No.', '#' + q.num], ['Topic', q.topic], ['Section', q.section]];
  if (q.tags.length) rows.push(['Tags', q.tags.join(', ')]);
  for (const [term, value] of rows) {
    if (!value) continue;
    const dt = document.createElement('dt'); dt.textContent = term;
    const dd = document.createElement('dd'); dd.textContent = value;
    dl.append(dt, dd);
  }
  detail.appendChild(dl);

  if (q.links.length) {
    const box = document.createElement('div');
    box.className = 'conn';
    const lab = document.createElement('div');
    lab.className = 'label';
    lab.textContent = q.links.length + ' cross-links';
    box.appendChild(lab);
    const ul = document.createElement('ul');
    for (const id of q.links) {
      const other = BY_ID.get(id);
      if (!other) continue;
      const li = document.createElement('li');
      const b = document.createElement('button');
      b.type = 'button';
      b.textContent = other.title;
      b.addEventListener('click', () => select(other));
      li.appendChild(b);
      ul.appendChild(li);
    }
    box.appendChild(ul);
    detail.appendChild(box);
  }

  const a = document.createElement('a');
  a.className = 'source-link';
  a.href = DATA.repoBlob + q.url.replace('./', '');
  a.target = '_blank';
  a.rel = 'noopener';
  a.textContent = 'Read the answer ↗';
  detail.appendChild(a);

  history.replaceState(null, '', '#' + q.id.replace(':', '-'));
  paint();
}

function clearSelection() {
  selected = null;
  detail.classList.remove('open');
  detail.replaceChildren();
  const p = document.createElement('p');
  p.className = 'empty-state';
  p.textContent = 'Select a question on the rim to see its topic, difficulty and cross-links.';
  detail.appendChild(p);
  history.replaceState(null, '', location.pathname + location.search);
  paint();
}

/* --------------------------------- Search -------------------------------- */
const search = document.getElementById('search');
search.addEventListener('input', e => {
  query = e.target.value.toLowerCase().trim();
  paint();

  if (!query) { renderResults([]); return; }
  renderResults(Q.filter(inScope).slice(0, 12));
});

function renderResults(list) {
  if (!list.length) {
    if (!selected) clearSelection();
    return;
  }
  detail.replaceChildren();
  detail.classList.add('open');
  const lab = document.createElement('div');
  lab.className = 'label';
  lab.textContent = list.length + ' matches';
  detail.appendChild(lab);
  const ul = document.createElement('ul');
  ul.id = 'results';
  for (const q of list) {
    const li = document.createElement('li');
    const b = document.createElement('button');
    b.type = 'button';
    b.textContent = '#' + q.num + '  ' + q.title;
    b.addEventListener('click', () => select(q));
    li.appendChild(b);
    ul.appendChild(li);
  }
  detail.appendChild(ul);
}

document.getElementById('reset').addEventListener('click', () => {
  SECTIONS.forEach(s => activeSections.add(s));
  LEVELS.forEach(l => activeLevels.add(l));
  document.querySelectorAll('.chip').forEach(c => c.setAttribute('aria-pressed', 'true'));
  search.value = '';
  query = '';
  clearSelection();
  search.focus();
});

/* --------------------------- Pan, zoom, keyboard -------------------------- */
let tx = 0, ty = 0, k = 1;
function applyTransform() {
  if (scene) scene.setAttribute('transform', `translate(${tx} ${ty}) scale(${k})`);
}
function zoomBy(factor, ox, oy) {
  const box = svg.getBoundingClientRect();
  const px = ox === undefined ? box.width / 2 : ox;
  const py = oy === undefined ? box.height / 2 : oy;
  const next = Math.min(6, Math.max(0.4, k * factor));
  // Keep the point under the cursor fixed while scaling.
  tx = px - (px - tx) * (next / k);
  ty = py - (py - ty) * (next / k);
  k = next;
  applyTransform();
}

svg.addEventListener('wheel', e => {
  e.preventDefault();
  const box = svg.getBoundingClientRect();
  zoomBy(e.deltaY < 0 ? 1.12 : 1 / 1.12, e.clientX - box.left, e.clientY - box.top);
}, { passive: false });

let dragging = false, lastX = 0, lastY = 0;
svg.addEventListener('pointerdown', e => {
  if (e.target.classList.contains('node')) return;
  dragging = true; lastX = e.clientX; lastY = e.clientY;
  scene && scene.classList.add('dragging');
  svg.setPointerCapture(e.pointerId);
});
svg.addEventListener('pointermove', e => {
  if (!dragging) return;
  tx += e.clientX - lastX; ty += e.clientY - lastY;
  lastX = e.clientX; lastY = e.clientY;
  applyTransform();
});
svg.addEventListener('pointerup', e => {
  dragging = false;
  scene && scene.classList.remove('dragging');
  try { svg.releasePointerCapture(e.pointerId); } catch (err) { /* already released */ }
});

document.getElementById('zoom-in').addEventListener('click', () => zoomBy(1.3));
document.getElementById('zoom-out').addEventListener('click', () => zoomBy(1 / 1.3));
document.getElementById('zoom-reset').addEventListener('click', () => { tx = 0; ty = 0; k = 1; applyTransform(); });

document.addEventListener('keydown', e => {
  const t = document.activeElement;
  const typing = t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable);
  if (e.key === '/' && !typing) { e.preventDefault(); search.focus(); return; }
  if (e.key === 'Escape') {
    if (selected) { clearSelection(); return; }
    if (search.value) { search.value = ''; query = ''; paint(); clearSelection(); }
  }
});

/* --------------------------------- Theme --------------------------------- */
const THEME_KEY = 'ai-eng-graph-theme';
const systemDark = matchMedia('(prefers-color-scheme: dark)');
const themeButtons = [...document.querySelectorAll('.theme-btn')];
let themeMode = document.documentElement.getAttribute('data-theme-mode') || 'system';

function applyTheme(mode, persist) {
  themeMode = mode;
  const effective = mode === 'system' ? (systemDark.matches ? 'dark' : 'light') : mode;
  document.documentElement.setAttribute('data-theme-mode', mode);
  document.documentElement.setAttribute('data-theme', effective);
  if (persist) { try { localStorage.setItem(THEME_KEY, mode); } catch (e) { /* private mode */ } }
  themeButtons.forEach(b => {
    const on = b.dataset.themeChoice === mode;
    b.setAttribute('aria-checked', String(on));
    b.tabIndex = on ? 0 : -1;
  });
  restyle();
}

/* SVG cannot read CSS custom properties for fill/stroke values that came from
   the data, so the scene keeps its own palette and is repainted on theme change.
   The glow is also cut right down in light: a blurred bright bead on a near-white
   ground reads as a smudge rather than a light. */
function restyle() {
  toneCache.clear();
  if (glowBlur) glowBlur.setAttribute('stdDeviation', isLight() ? '1.1' : '2.2');
  for (const { band, topic } of bands) band.setAttribute('stroke', tone(DATA.topics[topic].color));
  for (const { q, dot } of dots) dot.setAttribute('fill', tone(q.color));
  for (const link of wires) {
    const src = BY_ID.get(link.a);
    if (src) link.pulse.setAttribute('stroke', tone(DATA.topics[src.topic].color));
  }
  for (const b of document.querySelectorAll('.chip .dot')) {
    if (b.dataset.baseColor) b.style.background = tone(b.dataset.baseColor);
  }
}
themeButtons.forEach((b, i) => {
  b.addEventListener('click', () => applyTheme(b.dataset.themeChoice, true));
  b.addEventListener('keydown', e => {
    const d = (e.key === 'ArrowRight' || e.key === 'ArrowDown') ? 1
            : (e.key === 'ArrowLeft' || e.key === 'ArrowUp') ? -1 : 0;
    if (!d) return;
    e.preventDefault();
    const next = themeButtons[(i + d + themeButtons.length) % themeButtons.length];
    next.focus();
    applyTheme(next.dataset.themeChoice, true);
  });
});
systemDark.addEventListener('change', () => { if (themeMode === 'system') applyTheme('system', false); });
applyTheme(themeMode, false);

/* --------------------------------- Boot ---------------------------------- */
let resizeTimer;
addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(build, 150);
});

build();

// Deep link: /#q-181 opens that question directly.
const raw = location.hash.replace('#', '');
if (raw) {
  const node = BY_ID.get(raw.replace('-', ':'));
  if (node) select(node);
}
</script>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", "-o", default="docs/index.html", help="Target output HTML file path")
    args = parser.parse_args()

    view = flatten(build_graph_data())

    payload = json.dumps(view, indent=None)
    # Neutralise HTML-significant characters so no string in the data can close
    # the <script> element it is embedded in.
    payload = (payload.replace("<", r"\u003c")
                      .replace(">", r"\u003e")
                      .replace("&", r"\u0026"))

    html = (HTML_TEMPLATE
            .replace("__DATA__", payload)
            .replace("__QUESTION_COUNT__", str(len(view["questions"])))
            .replace("__TOPIC_COUNT__", str(len(view["topicOrder"])))
            .replace("__LINK_COUNT__", str(view["crossLinks"])))

    output_path = REPO_ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")

    print(f"Successfully generated AI Engineering Knowledge Graph at: {output_path}")
    print(f"Questions: {len(view['questions'])}, Topics: {len(view['topicOrder'])}, Cross-links: {view['crossLinks']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
