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


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI Engineering Knowledge Graph</title>

  <!-- Resolve the theme before first paint so the page never flashes the
       wrong palette. Must stay inline and ahead of the stylesheet. -->
  <script>
    (function () {{
      var mode;
      try {{ mode = localStorage.getItem('ai-eng-graph-theme'); }} catch (e) {{ /* private mode */ }}
      if (mode !== 'light' && mode !== 'dark' && mode !== 'system') mode = 'system';
      var effective = mode === 'system'
        ? (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
        : mode;
      var root = document.documentElement;
      root.setAttribute('data-theme-mode', mode);
      root.setAttribute('data-theme', effective);
    }})();
  </script>

  <link rel="preconnect" href="https://unpkg.com" crossorigin>
  <script src="https://unpkg.com/3d-force-graph@1.73.3/dist/3d-force-graph.min.js" integrity="sha384-SIcVySj+Cd1g+cwoLNCdr/osXU15HLXCxfaSzFNkZICYeKS7I2YxhyggCijT8JHA" crossorigin="anonymous"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600;700&display=swap');

    /* ---------------------------------------------------------------
       Theme tokens. Light is the bare :root default; dark is layered on
       twice so both the "system" default and an explicit toggle win:
         - @media (prefers-color-scheme: dark) for mode=system
         - [data-theme="dark"] for an explicit choice
       Every colour below is a token so the toggle needs no JS per rule.
       --------------------------------------------------------------- */
    :root {{
      --bg: #eef2f7;
      --panel-bg: rgba(255, 255, 255, 0.92);
      --panel-border: #cbd5e1;
      --panel-shadow: 0 20px 30px -10px rgba(15, 23, 42, 0.18), 0 0 15px rgba(8, 145, 178, 0.10);
      --text-strong: #0f172a;
      --text-body: #1e293b;
      --text-muted: #475569;
      --text-dim: #475569;
      --text-legend: #334155;
      --accent: #0891b2;
      --accent-fg: #0e7490;
      --accent-soft-bg: rgba(8, 145, 178, 0.12);
      --accent-soft-border: rgba(8, 145, 178, 0.35);
      --accent-hover-bg: rgba(8, 145, 178, 0.14);
      --accent-ring: rgba(8, 145, 178, 0.25);
      --input-bg: #ffffff;
      --input-border: #cbd5e1;
      --result-bg: #f8fafc;
      --divider: rgba(100, 116, 139, 0.35);
      --btn-bg: #0369a1;
      --btn-bg-hover: #075985;
      --btn-fg: #ffffff;
      --ghost-hover-bg: #e2e8f0;
      --tag-alpha: 0.10;
      --tag-topic-fg: #0e7490;
      --tag-question-fg: #1d4ed8;
      --tag-beginner-fg: #047857;
      --tag-intermediate-fg: #92400e;
      --tag-advanced-fg: #b91c1c;
      --tag-domain-fg: #6d28d9;
      --tag-general-fg: #475569;
    }}

    /* mode=system, OS is dark */
    @media (prefers-color-scheme: dark) {{
      :root:not([data-theme="light"]) {{
        --bg: #0b0f19;
        --panel-bg: rgba(15, 23, 42, 0.90);
        --panel-border: #334155;
        --panel-shadow: 0 20px 30px -10px rgba(0, 0, 0, 0.65), 0 0 18px rgba(6, 182, 212, 0.12);
        --text-strong: #f8fafc;
        --text-body: #e2e8f0;
        --text-muted: #94a3b8;
        --text-dim: #94a3b8;
        --text-legend: #cbd5e1;
        --accent: #06b6d4;
        --accent-fg: #22d3ee;
        --accent-soft-bg: rgba(6, 182, 212, 0.12);
        --accent-soft-border: rgba(6, 182, 212, 0.3);
        --accent-hover-bg: rgba(6, 182, 212, 0.2);
        --accent-ring: rgba(6, 182, 212, 0.2);
        --input-bg: rgba(30, 41, 59, 0.8);
        --input-border: #334155;
        --result-bg: rgba(30, 41, 59, 0.6);
        --divider: rgba(51, 65, 85, 0.5);
        --btn-bg: #0284c7;
        --btn-bg-hover: #0369a1;
        --btn-fg: #ffffff;
        --ghost-hover-bg: #1e293b;
        --tag-alpha: 0.15;
        --tag-topic-fg: #22d3ee;
        --tag-question-fg: #60a5fa;
        --tag-beginner-fg: #34d399;
        --tag-intermediate-fg: #fbbf24;
        --tag-advanced-fg: #f87171;
        --tag-domain-fg: #c084fc;
        --tag-general-fg: #cbd5e1;
      }}
    }}

    /* explicit dark choice — must also win when the OS is light */
    :root[data-theme="dark"] {{
      --bg: #0b0f19;
      --panel-bg: rgba(15, 23, 42, 0.90);
      --panel-border: #334155;
      --panel-shadow: 0 20px 30px -10px rgba(0, 0, 0, 0.65), 0 0 18px rgba(6, 182, 212, 0.12);
      --text-strong: #f8fafc;
      --text-body: #e2e8f0;
      --text-muted: #94a3b8;
      --text-dim: #94a3b8;
      --text-legend: #cbd5e1;
      --accent: #06b6d4;
      --accent-fg: #22d3ee;
      --accent-soft-bg: rgba(6, 182, 212, 0.12);
      --accent-soft-border: rgba(6, 182, 212, 0.3);
      --accent-hover-bg: rgba(6, 182, 212, 0.2);
      --accent-ring: rgba(6, 182, 212, 0.2);
      --input-bg: rgba(30, 41, 59, 0.8);
      --input-border: #334155;
      --result-bg: rgba(30, 41, 59, 0.6);
      --divider: rgba(51, 65, 85, 0.5);
      --btn-bg: #0284c7;
      --btn-bg-hover: #0369a1;
      --btn-fg: #ffffff;
      --ghost-hover-bg: #1e293b;
      --tag-alpha: 0.15;
      --tag-topic-fg: #22d3ee;
      --tag-question-fg: #60a5fa;
      --tag-beginner-fg: #34d399;
      --tag-intermediate-fg: #fbbf24;
      --tag-advanced-fg: #f87171;
      --tag-domain-fg: #c084fc;
      --tag-general-fg: #cbd5e1;
    }}

    * {{
      box-sizing: border-box;
    }}
    body {{
      margin: 0;
      padding: 0;
      background-color: var(--bg);
      color: var(--text-body);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      overflow: hidden;
      -webkit-text-size-adjust: 100%;
    }}
    
    /* Header Panel */
    #header {{
      position: absolute;
      top: 20px;
      left: 20px;
      z-index: 20;
      background: var(--panel-bg);
      padding: 18px 22px;
      border-radius: 12px;
      border: 1px solid var(--panel-border);
      backdrop-filter: blur(12px);
      max-width: 380px;
      box-shadow: var(--panel-shadow);
    }}
    .header-top {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 10px;
      margin-bottom: 8px;
    }}
    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 3px 8px;
      border-radius: 6px;
      background: var(--accent-soft-bg);
      color: var(--accent-fg);
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      border: 1px solid var(--accent-soft-border);
    }}
    .badge-dot {{
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--accent);
      box-shadow: 0 0 8px var(--accent);
    }}
    h1 {{
      margin: 0 0 8px 0;
      font-size: 1.25rem;
      font-weight: 700;
      color: var(--text-strong);
      letter-spacing: -0.3px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    p {{
      margin: 0 0 12px 0;
      font-size: 0.84rem;
      color: var(--text-muted);
      line-height: 1.45;
    }}

    /* Theme switcher (segmented radiogroup: light / dark / system) */
    #theme-switch {{
      display: flex;
      gap: 2px;
      padding: 2px;
      border-radius: 8px;
      background: var(--result-bg);
      border: 1px solid var(--input-border);
      flex-shrink: 0;
    }}
    .theme-btn {{
      display: flex;
      align-items: center;
      justify-content: center;
      width: 28px;
      height: 26px;
      padding: 0;
      border: none;
      border-radius: 6px;
      background: transparent;
      color: var(--text-muted);
      font-size: 0.85rem;
      line-height: 1;
      cursor: pointer;
      transition: background 0.15s ease, color 0.15s ease;
    }}
    .theme-btn:hover {{
      background: var(--accent-hover-bg);
      color: var(--text-strong);
    }}
    .theme-btn[aria-checked="true"] {{
      background: var(--accent-soft-bg);
      color: var(--accent-fg);
      box-shadow: inset 0 0 0 1px var(--accent-soft-border);
    }}
    .theme-btn:focus-visible {{
      outline: 2px solid var(--accent);
      outline-offset: 1px;
    }}

    /* Search Bar */
    .search-box {{
      position: relative;
      margin-bottom: 12px;
    }}
    .search-box input {{
      width: 100%;
      padding: 8px 12px 8px 34px;
      background: var(--input-bg);
      border: 1px solid var(--input-border);
      border-radius: 8px;
      color: var(--text-strong);
      font-family: 'Inter', sans-serif;
      font-size: 0.82rem;
      outline: none;
      transition: all 0.2s ease;
    }}
    .search-box input::placeholder {{
      color: var(--text-dim);
    }}
    .search-box input:focus {{
      border-color: var(--accent);
      box-shadow: 0 0 0 2px var(--accent-ring);
    }}
    .search-icon {{
      position: absolute;
      left: 10px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-dim);
      font-size: 0.85rem;
    }}

    /* Search Results List */
    #search-results {{
      max-height: 200px;
      overflow-y: auto;
      margin-bottom: 12px;
      display: none;
    }}
    #search-results.visible {{
      display: block;
    }}
    #search-results ul {{
      list-style: none;
      margin: 0;
      padding: 0;
    }}
    #search-results li {{
      margin: 0;
      padding: 0;
    }}
    #search-results button {{
      width: 100%;
      text-align: left;
      background: var(--result-bg);
      border: 1px solid var(--input-border);
      color: var(--text-body);
      padding: 6px 10px;
      margin-bottom: 3px;
      border-radius: 6px;
      font-family: 'Inter', sans-serif;
      font-size: 0.78rem;
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    #search-results button:hover {{
      background: var(--accent-hover-bg);
      border-color: var(--accent);
    }}
    #search-results button:focus {{
      outline: 2px solid var(--accent);
      outline-offset: -1px;
    }}

    /* Legend */
    .legend {{
      display: flex;
      gap: 12px;
      font-size: 0.78rem;
      flex-wrap: wrap;
      padding-top: 8px;
      border-top: 1px solid var(--divider);
    }}
    .legend-item {{
      display: flex;
      align-items: center;
      gap: 6px;
      color: var(--text-legend);
    }}
    .dot {{
      width: 9px;
      height: 9px;
      border-radius: 50%;
      display: inline-block;
    }}

    /* Stats Bar */
    .stats-bar {{
      display: flex;
      justify-content: space-between;
      margin-top: 10px;
      padding-top: 8px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.75rem;
      color: var(--text-dim);
      border-top: 1px dashed var(--divider);
    }}

    #graph {{
      width: 100%;
      height: 100vh;
      height: 100dvh;
    }}

    /* ---------------------------------------------------------------
       Bottom-right stack: inspector card above the zoom controls.
       Both used to want the same corner, so they are flex siblings in
       one positioned wrapper — flow guarantees they cannot overlap.
       The wrapper is pointer-transparent so its empty area (the gap and
       the strip beside the buttons) still rotates the graph.
       --------------------------------------------------------------- */
    #bottom-right {{
      position: absolute;
      bottom: 24px;
      right: 24px;
      z-index: 20;
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      gap: 12px;
      pointer-events: none;
    }}
    #bottom-right > * {{
      pointer-events: auto;
    }}

    /* Zoom controls */
    #zoom-controls {{
      display: flex;
      flex-direction: column;
      gap: 6px;
      flex-shrink: 0;
    }}
    .zoom-btn {{
      display: flex;
      align-items: center;
      justify-content: center;
      width: 44px;
      height: 44px;
      padding: 0;
      border-radius: 10px;
      border: 1px solid var(--panel-border);
      background: var(--panel-bg);
      color: var(--text-strong);
      backdrop-filter: blur(12px);
      box-shadow: var(--panel-shadow);
      font-size: 1.35rem;
      font-weight: 500;
      line-height: 1;
      cursor: pointer;
      transition: background 0.15s ease, border-color 0.15s ease;
    }}
    .zoom-btn:hover {{
      background: var(--accent-hover-bg);
      border-color: var(--accent);
    }}
    .zoom-btn:focus-visible {{
      outline: 2px solid var(--accent);
      outline-offset: 2px;
    }}

    /* Floating Inspector Card */
    #info-card {{
      background: var(--panel-bg);
      padding: 18px 22px;
      border-radius: 14px;
      border: 1px solid var(--panel-border);
      display: none;
      width: 360px;
      box-shadow: var(--panel-shadow);
      backdrop-filter: blur(12px);
      animation: slideUp 0.25s ease-out;
    }}
    @keyframes slideUp {{
      from {{ opacity: 0; transform: translateY(12px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    .card-meta {{
      display: flex;
      gap: 6px;
      margin-bottom: 10px;
    }}
    /* Tag colours are driven by data attributes rather than inline styles
       so each theme can set its own accessible foreground. */
    .card-tag {{
      padding: 2px 8px;
      border-radius: 4px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.7rem;
      font-weight: 600;
      text-transform: uppercase;
      color: var(--tag-general-fg);
      background: var(--result-bg);
      background: color-mix(in srgb, currentColor calc(var(--tag-alpha) * 100%), transparent);
    }}
    .card-tag[data-kind="topic"] {{ color: var(--tag-topic-fg); }}
    .card-tag[data-kind="question"] {{ color: var(--tag-question-fg); }}
    .card-tag[data-level="beginner"] {{ color: var(--tag-beginner-fg); }}
    .card-tag[data-level="intermediate"] {{ color: var(--tag-intermediate-fg); }}
    .card-tag[data-level="advanced"] {{ color: var(--tag-advanced-fg); }}
    .card-tag[data-level="domain"] {{ color: var(--tag-domain-fg); }}
    .card-tag[data-level="general"] {{ color: var(--tag-general-fg); }}

    #info-card h3 {{
      margin: 0 0 8px 0;
      font-size: 1.05rem;
      font-weight: 600;
      color: var(--text-strong);
      line-height: 1.35;
    }}
    #info-card p {{
      margin: 0 0 14px 0;
      color: var(--text-legend);
      font-size: 0.82rem;
      line-height: 1.45;
    }}
    .card-actions {{
      display: flex;
      gap: 8px;
    }}
    #card-link {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: var(--btn-bg);
      color: var(--btn-fg);
      padding: 8px 14px;
      border-radius: 8px;
      text-decoration: none;
      font-size: 0.8rem;
      font-weight: 600;
      transition: all 0.2s ease;
      box-shadow: 0 4px 12px var(--accent-ring);
    }}
    #card-link:hover {{
      background: var(--btn-bg-hover);
      transform: translateY(-1px);
    }}
    #card-link:focus-visible, .close-btn:focus-visible {{
      outline: 2px solid var(--accent);
      outline-offset: 2px;
    }}
    .close-btn {{
      background: transparent;
      border: 1px solid var(--input-border);
      color: var(--text-muted);
      border-radius: 8px;
      padding: 8px 12px;
      cursor: pointer;
      font-size: 0.8rem;
    }}
    .close-btn:hover {{
      background: var(--ghost-hover-bg);
      color: var(--text-strong);
    }}

    /* ---------------------------------------------------------------
       Mobile / narrow viewports.

       Both panels are fixed-position overlays on a full-bleed canvas,
       so on a small screen they grow into each other: the header grows
       downward as search results populate while the info card grows
       upward from the bottom. Capping the header at 40dvh from the top
       and the card at 45dvh from the bottom leaves a 15dvh gutter, so
       they can never meet no matter how much content either holds.
       --------------------------------------------------------------- */
    @media (max-width: 768px) {{
      #header {{
        top: 10px;
        left: 10px;
        right: 10px;
        max-width: none;
        max-height: 40dvh;
        overflow-y: auto;
        -webkit-overflow-scrolling: touch;
        overscroll-behavior: contain;
        padding: 14px 16px;
      }}
      /* Decorative on a small screen; the graph itself is the explanation. */
      #header > p {{
        display: none;
      }}
      h1 {{
        font-size: 1.05rem;
      }}
      /* Must be >= 16px or iOS Safari zooms the whole page on focus. */
      .search-box input {{
        font-size: 16px;
        padding: 10px 12px 10px 34px;
      }}
      #search-results {{
        max-height: 34vh;
      }}
      /* WCAG 2.2 target size (2.5.8) + comfortable thumb target. */
      #search-results button {{
        min-height: 44px;
        font-size: 0.85rem;
      }}

      #bottom-right {{
        bottom: 10px;
        left: 10px;
        right: 10px;
        max-height: 45dvh;
      }}
      #info-card {{
        width: 100%;
        min-height: 0;
        overflow-y: auto;
        -webkit-overflow-scrolling: touch;
        overscroll-behavior: contain;
        padding: 16px;
      }}
      .card-actions {{
        flex-wrap: wrap;
      }}
      #card-link, .close-btn {{
        min-height: 44px;
        align-items: center;
        display: inline-flex;
      }}
    }}

    /* Landscape phones: vertical space is the binding constraint, so drop
       everything non-essential rather than shrinking both panels further. */
    @media (max-height: 500px) and (orientation: landscape) {{
      #header {{
        max-height: 60dvh;
        max-width: 320px;
        right: auto;
      }}
      #header > p, .legend, .stats-bar {{
        display: none;
      }}
      #bottom-right {{
        max-height: 62dvh;
        left: auto;
      }}
      #info-card {{
        width: 320px;
      }}
    }}

    /* 3d-force-graph injects a "Left-click: rotate, Mouse-wheel: zoom" hint.
       It describes controls that do not exist on a touch device, and it sits
       under the info card at the bottom edge. Drop it where there is no mouse. */
    @media (hover: none) and (pointer: coarse) {{
      .scene-nav-info {{
        display: none;
      }}
    }}

    @media (prefers-reduced-motion: reduce) {{
      #info-card {{
        animation: none;
      }}
      #card-link:hover {{
        transform: none;
      }}
    }}

    /* ------------------------------------------------------------------
       Filters, metadata panel, and connection list.
       Colours are tokens only -- both themes follow the switcher for free.
       ------------------------------------------------------------------ */
    .filter-group {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 10px;
    }}

    .filter-group-label {{
      width: 100%;
      font-size: 10px;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--text-dim);
      margin-bottom: 2px;
    }}

    .chip {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      font: inherit;
      font-size: 11px;
      line-height: 1.4;
      color: var(--text-legend);
      background: transparent;
      border: 1px solid var(--panel-border);
      border-radius: 999px;
      cursor: pointer;
      transition: background 120ms ease, border-color 120ms ease, opacity 120ms ease;
    }}

    .chip:hover {{ background: var(--ghost-hover-bg); }}

    .chip:focus-visible {{
      outline: 2px solid var(--accent);
      outline-offset: 2px;
    }}

    /* Unselected reads as muted, not hidden: the set stays legible. */
    .chip[aria-pressed="false"] {{ opacity: 0.45; }}

    .chip[aria-pressed="true"] {{
      background: var(--accent-soft-bg);
      border-color: var(--accent-soft-border);
      color: var(--text-strong);
    }}

    .chip .dot {{
      width: 9px;
      height: 9px;
      border-radius: 50%;
      flex: none;
    }}

    .chip .chip-count {{
      font-variant-numeric: tabular-nums;
      color: var(--text-dim);
    }}

    #filter-reset {{
      margin-left: auto;
      font-size: 10px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      background: none;
      border: none;
      color: var(--accent-fg);
      cursor: pointer;
      padding: 4px 2px;
    }}

    #filter-reset:focus-visible {{
      outline: 2px solid var(--accent);
      outline-offset: 2px;
    }}

    #match-count {{
      font-size: 11px;
      color: var(--text-dim);
      margin-top: 6px;
      font-variant-numeric: tabular-nums;
    }}

    .card-meta-list {{
      margin: 8px 0 0;
      display: grid;
      grid-template-columns: auto 1fr;
      gap: 3px 10px;
      font-size: 11.5px;
    }}

    .card-meta-list dt {{
      color: var(--text-dim);
      text-transform: uppercase;
      letter-spacing: 0.06em;
      font-size: 10px;
      align-self: center;
    }}

    .card-meta-list dd {{
      margin: 0;
      color: var(--text-body);
    }}

    .card-connections {{
      margin-top: 10px;
      border-top: 1px solid var(--divider);
      padding-top: 8px;
    }}

    .card-connections h4 {{
      margin: 0 0 5px;
      font-size: 10px;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--text-dim);
      font-weight: 600;
    }}

    .card-connections ul {{
      list-style: none;
      margin: 0;
      padding: 0;
      max-height: 132px;
      overflow-y: auto;
    }}

    .card-connections button {{
      display: block;
      width: 100%;
      text-align: left;
      font: inherit;
      font-size: 11.5px;
      line-height: 1.35;
      color: var(--accent-fg);
      background: none;
      border: none;
      border-radius: 4px;
      padding: 3px 4px;
      cursor: pointer;
    }}

    .card-connections button:hover {{ background: var(--ghost-hover-bg); }}

    .card-connections button:focus-visible {{
      outline: 2px solid var(--accent);
      outline-offset: -2px;
    }}

    .kbd {{
      display: inline-block;
      padding: 1px 5px;
      font-size: 10px;
      font-family: inherit;
      color: var(--text-dim);
      background: var(--result-bg);
      border: 1px solid var(--panel-border);
      border-radius: 4px;
    }}

    /* Respect the OS setting: the camera flights and particle streams are the
       motion-heavy parts, so they are cut rather than merely shortened. */
    @media (prefers-reduced-motion: reduce) {{
      .chip {{ transition: none; }}
    }}
  </style>
</head>
<body>
  <div id="header">
    <div class="header-top">
      <div class="badge"><span class="badge-dot"></span> Live Telemetry Topology</div>
      <div id="theme-switch" role="radiogroup" aria-label="Colour theme">
        <button type="button" class="theme-btn" role="radio" aria-checked="false"
                data-theme-choice="light" aria-label="Light theme" title="Light theme">☀</button>
        <button type="button" class="theme-btn" role="radio" aria-checked="false"
                data-theme-choice="dark" aria-label="Dark theme" title="Dark theme">☾</button>
        <button type="button" class="theme-btn" role="radio" aria-checked="false"
                data-theme-choice="system" aria-label="Match system theme" title="Match system theme">◐</button>
      </div>
    </div>
    <h1>⚡ AI Engineering Knowledge Graph</h1>
    <p>Interactive 3D map linking {question_count} AI engineering interview questions across {topic_count} topics, wired by explicit cross-links and [[wikilinks]].</p>
    
    <div class="search-box">
      <span class="search-icon">🔍</span>
      <input type="text" id="search-input" placeholder="Filter questions or topics (e.g. RAG, prompt injection, LoRA)...">
    </div>

    <div id="search-results" role="region" aria-label="Search results">
      <ul id="search-results-list"></ul>
    </div>

    <div class="filter-group" id="section-filters" role="group" aria-label="Filter by section">
      <span class="filter-group-label">Sections</span>
    </div>

    <div class="filter-group" id="difficulty-filters" role="group" aria-label="Filter by difficulty">
      <span class="filter-group-label">Difficulty</span>
      <button type="button" id="filter-reset">Reset</button>
    </div>

    <p id="match-count" role="status" aria-live="polite"></p>

    <div class="stats-bar">
      <span>NODES: <strong id="node-count">0</strong></span>
      <span>EDGES: <strong id="edge-count">0</strong></span>
      <span>TOPICS: <strong id="topic-count">0</strong></span>
      <span class="kbd-hint"><span class="kbd">/</span> search · <span class="kbd">Esc</span> clear</span>
    </div>
  </div>

  <div id="bottom-right">
    <div id="info-card">
      <div class="card-meta">
        <span id="card-type" class="card-tag" data-kind="question">QUESTION</span>
        <span id="card-difficulty" class="card-tag" data-level="beginner">BEGINNER</span>
      </div>
      <h3 id="card-title">Node Info</h3>
      <dl class="card-meta-list" id="card-meta-list"></dl>
      <div class="card-connections" id="card-connections" hidden>
        <h4 id="card-connections-heading">Connected questions</h4>
        <ul id="card-connections-list" aria-labelledby="card-connections-heading"></ul>
      </div>
      <div class="card-actions">
        <a id="card-link" href="#" target="_blank" rel="noopener">View Markdown Source ↗</a>
        <button type="button" class="close-btn" id="card-dismiss">Dismiss</button>
      </div>
    </div>

    <div id="zoom-controls" role="group" aria-label="Zoom controls">
      <button type="button" class="zoom-btn" id="zoom-in" aria-label="Zoom in">+</button>
      <button type="button" class="zoom-btn" id="zoom-out" aria-label="Zoom out">−</button>
    </div>
  </div>

  <div id="graph"></div>

  <script>
    const gData = {graph_json};

    const QUESTION_NODES = gData.nodes.filter(n => n.type === 'question');
    const TOPIC_NODES = gData.nodes.filter(n => n.type === 'topic');

    document.getElementById('node-count').innerText = gData.nodes.length;
    document.getElementById('edge-count').innerText = gData.links.length;
    document.getElementById('topic-count').innerText = TOPIC_NODES.length;

    const REDUCED_MOTION = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // Adjacency, built once. Powers the "connected questions" list in the
    // detail panel -- the cross-links are the point of the graph, so they
    // belong in the panel rather than only as edges you have to trace by eye.
    const NODE_BY_ID = new Map(gData.nodes.map(n => [n.id, n]));
    const NEIGHBOURS = new Map(gData.nodes.map(n => [n.id, new Set()]));
    for (const link of gData.links) {{
      const src = typeof link.source === 'object' ? link.source.id : link.source;
      const tgt = typeof link.target === 'object' ? link.target.id : link.target;
      if (link.type !== 'cross-link') continue;
      NEIGHBOURS.get(src) && NEIGHBOURS.get(src).add(tgt);
      NEIGHBOURS.get(tgt) && NEIGHBOURS.get(tgt).add(src);
    }}

    // Section and difficulty facets are DERIVED FROM THE DATA, never hardcoded.
    // A new topic group or difficulty in the repo shows up here on the next
    // build with no edit to this template -- which is exactly how the old
    // "TOPICS: 40" and the DevOps colour keys silently went stale.
    const SECTIONS = [...new Set(gData.nodes.map(n => n.section).filter(Boolean))].sort();
    const DIFFICULTIES = ['Beginner', 'Intermediate', 'Advanced']
      .filter(d => QUESTION_NODES.some(n => n.difficulty === d));

    const SECTION_COLOR = new Map();
    for (const t of TOPIC_NODES) {{
      if (t.section && !SECTION_COLOR.has(t.section)) SECTION_COLOR.set(t.section, t.color);
    }}
    const DIFFICULTY_COLOR = new Map();
    for (const q of QUESTION_NODES) {{
      if (q.difficulty && !DIFFICULTY_COLOR.has(q.difficulty)) DIFFICULTY_COLOR.set(q.difficulty, q.color);
    }}

    const activeSections = new Set(SECTIONS);
    const activeDifficulties = new Set(DIFFICULTIES);

    function buildChip(label, count, color, isOn, onToggle) {{
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'chip';
      btn.setAttribute('aria-pressed', String(isOn));
      if (color) {{
        const dot = document.createElement('span');
        dot.className = 'dot';
        dot.style.background = color;
        btn.appendChild(dot);
      }}
      btn.appendChild(document.createTextNode(label));
      const tally = document.createElement('span');
      tally.className = 'chip-count';
      tally.textContent = String(count);
      btn.appendChild(tally);
      btn.addEventListener('click', () => {{
        const next = btn.getAttribute('aria-pressed') !== 'true';
        btn.setAttribute('aria-pressed', String(next));
        onToggle(next);
        applyFilters();
      }});
      return btn;
    }}

    const sectionRail = document.getElementById('section-filters');
    for (const section of SECTIONS) {{
      const count = QUESTION_NODES.filter(n => n.section === section).length;
      sectionRail.appendChild(buildChip(section, count, SECTION_COLOR.get(section), true, on => {{
        on ? activeSections.add(section) : activeSections.delete(section);
      }}));
    }}

    const difficultyRail = document.getElementById('difficulty-filters');
    const resetBtn = document.getElementById('filter-reset');
    for (const level of DIFFICULTIES) {{
      const count = QUESTION_NODES.filter(n => n.difficulty === level).length;
      difficultyRail.insertBefore(
        buildChip(level, count, DIFFICULTY_COLOR.get(level), true, on => {{
          on ? activeDifficulties.add(level) : activeDifficulties.delete(level);
        }}),
        resetBtn
      );
    }}

    const card = document.getElementById('info-card');
    const cardType = document.getElementById('card-type');
    const cardDifficulty = document.getElementById('card-difficulty');
    const cardTitle = document.getElementById('card-title');
    const cardLink = document.getElementById('card-link');
    const cardMetaList = document.getElementById('card-meta-list');
    const cardConnections = document.getElementById('card-connections');
    const cardConnectionsList = document.getElementById('card-connections-list');
    const searchResults = document.getElementById('search-results');
    const searchResultsList = document.getElementById('search-results-list');

    // Node click handler (shared for graph clicks and list item activation)
    function handleNodeActivation(node) {{
      if (!node) return;

      const distance = 120;
      const distRatio = 1 + distance/Math.hypot(node.x, node.y, node.z);
      Graph.cameraPosition(
        {{ x: node.x * distRatio, y: node.y * distRatio, z: node.z * distRatio }},
        node,
        REDUCED_MOTION ? 0 : 2000
      );

      // Tag colours come from theme tokens keyed off these data attributes,
      // so both light and dark get an accessible foreground automatically.
      if (node.type === 'topic') {{
        cardType.innerText = 'TOPIC HUB';
        cardType.dataset.kind = 'topic';
        cardDifficulty.innerText = node.section || 'DOMAIN';
        cardDifficulty.dataset.level = 'domain';
      }} else {{
        cardType.innerText = 'QUESTION';
        cardType.dataset.kind = 'question';
        cardDifficulty.innerText = (node.difficulty || 'GENERAL').toUpperCase();
        const levels = {{ Beginner: 'beginner', Intermediate: 'intermediate', Advanced: 'advanced' }};
        cardDifficulty.dataset.level = levels[node.difficulty] || 'general';
      }}

      cardTitle.innerText = node.title || node.label;

      // Structured rows beat a newline-joined blob: screen readers get real
      // term/definition pairs, and long values wrap instead of overflowing.
      const rows = [
        ['Section', node.section],
        ['Topic', node.category],
        ['Difficulty', node.type === 'question' ? node.difficulty : null],
        ['Tags', Array.isArray(node.tags)
          ? node.tags.filter(t => t !== 'ai-engineering' && t !== 'interview-questions').join(', ')
          : null]
      ].filter(([, value]) => value);

      cardMetaList.replaceChildren();
      for (const [term, value] of rows) {{
        const dt = document.createElement('dt');
        dt.textContent = term;
        const dd = document.createElement('dd');
        dd.textContent = value;
        cardMetaList.append(dt, dd);
      }}

      const neighbours = [...(NEIGHBOURS.get(node.id) || [])]
        .map(id => NODE_BY_ID.get(id))
        .filter(Boolean)
        .sort((a, b) => (a.title || a.label).localeCompare(b.title || b.label));

      cardConnectionsList.replaceChildren();
      if (neighbours.length) {{
        for (const neighbour of neighbours) {{
          const li = document.createElement('li');
          const btn = document.createElement('button');
          btn.type = 'button';
          btn.textContent = neighbour.title || neighbour.label;
          btn.addEventListener('click', () => handleNodeActivation(neighbour));
          li.appendChild(btn);
          cardConnectionsList.appendChild(li);
        }}
        cardConnections.hidden = false;
      }} else {{
        cardConnections.hidden = true;
      }}

      cardLink.href = `https://github.com/mchittineni/ultimate-ai-engineering-guide/blob/main/${{node.url.replace('./', '')}}`;
      card.style.display = 'block';
      card.focus();
      if (node.type === 'question') {{
        history.replaceState(null, '', `#${{node.id.replace(':', '-')}}`);
      }}
    }}

    // The WebGL scene cannot read CSS variables, so the graph keeps its own
    // parallel palette. Light needs more link opacity because the data-supplied
    // link tints were picked against a near-black background.
    const GRAPH_THEME = {{
      dark: {{
        bg: '#0b0f19',
        link: 'rgba(148, 163, 184, 0.25)',
        linkOpacity: 0.35,
        dim: 'rgba(51, 65, 85, 0.30)',
        hit: '#38bdf8'
      }},
      light: {{
        bg: '#eef2f7',
        link: 'rgba(51, 65, 85, 0.45)',
        linkOpacity: 0.4,
        dim: 'rgba(148, 163, 184, 0.55)',
        hit: '#0369a1'
      }}
    }};

    let graphTheme = GRAPH_THEME[document.documentElement.getAttribute('data-theme')] || GRAPH_THEME.dark;

    const Graph = ForceGraph3D()
      (document.getElementById('graph'))
        .graphData(gData)
        .nodeId('id')
        .nodeVal('val')
        .nodeColor('color')
        .nodeLabel('label')
        .nodeResolution(16)
        .backgroundColor(graphTheme.bg)
        .linkOpacity(graphTheme.linkOpacity)
        .linkWidth(link => link.type === 'topic-link' ? 1.8 : 0.8)
        .linkColor(link => link.color || graphTheme.link)
        .linkDirectionalParticles(link => link.type === 'cross-link' ? 3 : 0)
        .linkDirectionalParticleWidth(2.0)
        .linkDirectionalParticleSpeed(0.006)
        .onNodeHover(node => {{
          document.body.style.cursor = node ? 'pointer' : 'default';
        }})
        .onNodeClick(handleNodeActivation);

    document.getElementById('card-dismiss').addEventListener('click', () => {{
      card.style.display = 'none';
    }});

    /* ----------------------------- Theme ----------------------------- */
    const THEME_KEY = 'ai-eng-graph-theme';
    const systemDark = window.matchMedia('(prefers-color-scheme: dark)');
    const themeButtons = Array.from(document.querySelectorAll('.theme-btn'));
    let themeMode = document.documentElement.getAttribute('data-theme-mode') || 'system';

    function applyTheme(mode, persist) {{
      themeMode = mode;
      const effective = mode === 'system' ? (systemDark.matches ? 'dark' : 'light') : mode;

      document.documentElement.setAttribute('data-theme-mode', mode);
      document.documentElement.setAttribute('data-theme', effective);

      if (persist) {{
        try {{ localStorage.setItem(THEME_KEY, mode); }} catch (e) {{ /* private mode */ }}
      }}

      themeButtons.forEach(btn => {{
        const on = btn.dataset.themeChoice === mode;
        btn.setAttribute('aria-checked', String(on));
        // Only the selected radio stays in the tab order.
        btn.tabIndex = on ? 0 : -1;
      }});

      graphTheme = GRAPH_THEME[effective];
      Graph.backgroundColor(graphTheme.bg);
      Graph.linkOpacity(graphTheme.linkOpacity);
      Graph.linkColor(link => link.color || graphTheme.link);
      paintNodes();
    }}

    themeButtons.forEach((btn, i) => {{
      btn.addEventListener('click', () => applyTheme(btn.dataset.themeChoice, true));
      // Arrow-key navigation, as expected of a radiogroup.
      btn.addEventListener('keydown', (evt) => {{
        const back = evt.key === 'ArrowLeft' || evt.key === 'ArrowUp';
        const fwd = evt.key === 'ArrowRight' || evt.key === 'ArrowDown';
        if (!back && !fwd) return;
        evt.preventDefault();
        const next = themeButtons[(i + (fwd ? 1 : -1) + themeButtons.length) % themeButtons.length];
        next.focus();
        applyTheme(next.dataset.themeChoice, true);
      }});
    }});

    // Follow the OS only while the user has chosen "system".
    systemDark.addEventListener('change', () => {{
      if (themeMode === 'system') applyTheme('system', false);
    }});

    /* ----------------------------- Zoom ----------------------------- */
    // Scale the camera's distance from the origin. Clamped so a long press
    // cannot bury the camera inside the cluster or lose the graph entirely.
    const ZOOM_STEP = 1.35;
    const MIN_DIST = 40;
    const MAX_DIST = 4000;

    function zoomByFactor(factor) {{
      const pos = Graph.cameraPosition();
      const dist = Math.hypot(pos.x, pos.y, pos.z);
      if (!dist) return;
      const target = Math.min(MAX_DIST, Math.max(MIN_DIST, dist * factor));
      const ratio = target / dist;
      Graph.cameraPosition(
        {{ x: pos.x * ratio, y: pos.y * ratio, z: pos.z * ratio }},
        undefined,
        220
      );
    }}

    document.getElementById('zoom-in').addEventListener('click', () => zoomByFactor(1 / ZOOM_STEP));
    document.getElementById('zoom-out').addEventListener('click', () => zoomByFactor(ZOOM_STEP));

    // Helper function to check if node matches query
    function nodeMatchesQuery(node, query) {{
      const label = (node.label || '').toLowerCase();
      const cat = (node.category || '').toLowerCase();
      const sec = (node.section || '').toLowerCase();
      const diff = (node.difficulty || '').toLowerCase();

      // Check tags array
      let tagsMatch = false;
      if (Array.isArray(node.tags)) {{
        tagsMatch = node.tags.some(tag => (tag || '').toLowerCase().includes(query));
      }} else if (typeof node.tags === 'string') {{
        tagsMatch = node.tags.toLowerCase().includes(query);
      }}

      return label.includes(query) || cat.includes(query) || sec.includes(query) || diff.includes(query) || tagsMatch;
    }}

    // Single owner of node colouring, so a theme switch mid-search repaints
    // the highlight/dim colours instead of stranding the old palette.
    let activeQuery = '';

    // A node is in scope when it clears BOTH facets and the text query.
    // Topic hubs follow their section only -- they have no difficulty.
    function nodeInScope(node) {{
      if (node.section && !activeSections.has(node.section)) return false;
      if (node.type === 'question' && node.difficulty && !activeDifficulties.has(node.difficulty)) return false;
      if (activeQuery && !nodeMatchesQuery(node, activeQuery)) return false;
      return true;
    }}

    const facetsWideOpen = () =>
      activeSections.size === SECTIONS.length && activeDifficulties.size === DIFFICULTIES.length;

    function paintNodes() {{
      if (!activeQuery && facetsWideOpen()) {{
        Graph.nodeColor(node => node.color);
        Graph.linkColor(link => link.color || graphTheme.link);
        return;
      }}
      // Out-of-scope nodes are dimmed rather than removed, so the shape of the
      // whole vault stays visible and the selection reads as a subset of it.
      Graph.nodeColor(node => {{
        if (!nodeInScope(node)) return graphTheme.dim;
        return activeQuery ? graphTheme.hit : node.color;
      }});
      Graph.linkColor(link => {{
        const src = typeof link.source === 'object' ? link.source : NODE_BY_ID.get(link.source);
        const tgt = typeof link.target === 'object' ? link.target : NODE_BY_ID.get(link.target);
        const lit = src && tgt && nodeInScope(src) && nodeInScope(tgt);
        return lit ? (link.color || graphTheme.link) : graphTheme.dim;
      }});
    }}

    const matchCount = document.getElementById('match-count');

    function applyFilters() {{
      paintNodes();
      const shown = QUESTION_NODES.filter(nodeInScope).length;
      matchCount.textContent = (shown === QUESTION_NODES.length && !activeQuery)
        ? `Showing all ${{QUESTION_NODES.length}} questions`
        : `Showing ${{shown}} of ${{QUESTION_NODES.length}} questions`;
    }}

    resetBtn.addEventListener('click', () => {{
      SECTIONS.forEach(sec => activeSections.add(sec));
      DIFFICULTIES.forEach(d => activeDifficulties.add(d));
      document.querySelectorAll('.chip').forEach(c => c.setAttribute('aria-pressed', 'true'));
      const input = document.getElementById('search-input');
      input.value = '';
      activeQuery = '';
      searchResults.classList.remove('visible');
      searchResultsList.replaceChildren();
      applyFilters();
      input.focus();
    }});

    // Live search filter
    document.getElementById('search-input').addEventListener('input', (e) => {{
      const query = e.target.value.toLowerCase().trim();
      activeQuery = query;
      if (!query) {{
        applyFilters();
        searchResults.classList.remove('visible');
        searchResultsList.replaceChildren();
        return;
      }}

      // Filter matching nodes
      const matchingNodes = gData.nodes.filter(nodeInScope);

      applyFilters();

      // Populate accessible search results list
      searchResultsList.replaceChildren();
      if (matchingNodes.length > 0) {{
        matchingNodes.slice(0, 20).forEach(node => {{
          const li = document.createElement('li');
          const btn = document.createElement('button');
          btn.textContent = node.label;
          btn.setAttribute('type', 'button');
          btn.addEventListener('click', () => handleNodeActivation(node));
          btn.addEventListener('keydown', (evt) => {{
            if (evt.key === 'Enter' || evt.key === ' ') {{
              evt.preventDefault();
              handleNodeActivation(node);
            }}
          }});
          li.appendChild(btn);
          searchResultsList.appendChild(li);
        }});
        searchResults.classList.add('visible');
      }} else {{
        searchResults.classList.remove('visible');
      }}
    }});

    /* -------------------------- Keyboard -------------------------- */
    // "/" focuses search and Escape clears -- the two shortcuts advertised in
    // the stats bar. Guarded so they never hijack typing in a field.
    document.addEventListener('keydown', (evt) => {{
      const el = document.activeElement;
      const typing = el && (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.isContentEditable);

      if (evt.key === '/' && !typing) {{
        evt.preventDefault();
        document.getElementById('search-input').focus();
        return;
      }}

      if (evt.key === 'Escape') {{
        if (card.style.display === 'block') {{
          card.style.display = 'none';
          history.replaceState(null, '', location.pathname + location.search);
          return;
        }}
        const input = document.getElementById('search-input');
        if (input.value) {{
          input.value = '';
          activeQuery = '';
          searchResults.classList.remove('visible');
          searchResultsList.replaceChildren();
          applyFilters();
        }}
      }}
    }});

    document.getElementById('card-dismiss').addEventListener('click', () => {{
      history.replaceState(null, '', location.pathname + location.search);
    }});

    // Physics Tuning
    Graph.d3Force('charge').strength(-130);

    // Deep link: /#q-181 opens that question once the layout has settled, so a
    // specific node can be shared or linked from a talk.
    (function restoreFromHash() {{
      const raw = location.hash.replace('#', '');
      if (!raw) return;
      const node = NODE_BY_ID.get(raw.replace('-', ':'));
      if (node) setTimeout(() => handleNodeActivation(node), REDUCED_MOTION ? 0 : 900);
    }})();

    applyFilters();

    // Sync the switcher's checked state and the scene palette with the mode
    // the pre-paint script already resolved. Not persisted: nothing changed yet.
    applyTheme(themeMode, false);
  </script>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", "-o", default="docs/index.html", help="Target output HTML file path")
    args = parser.parse_args()

    graph_data = build_graph_data()

    output_path = REPO_ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Escape HTML-significant characters in JSON to prevent script breakout
    json_str = json.dumps(graph_data, indent=2)
    json_str = json_str.replace('<', r'\u003c').replace('>', r'\u003e').replace('&', r'\u0026')

    question_count = sum(1 for n in graph_data["nodes"] if n.get("type") == "question")
    topic_count = sum(1 for n in graph_data["nodes"] if n.get("type") == "topic")

    html_content = HTML_TEMPLATE.format(
        graph_json=json_str,
        question_count=question_count,
        topic_count=topic_count,
    )
    output_path.write_text(html_content, encoding="utf-8")

    print(f"Successfully generated AI Engineering Knowledge Graph at: {output_path}")
    print(f"Nodes: {len(graph_data['nodes'])}, Edges: {len(graph_data['links'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())