#!/usr/bin/env python3
"""Generate an interactive HTML knowledge graph for GitHub Pages.

Parses all Markdown questions and topic indexes, extracts connections (categories,
shared tags, and explicit cross-file relative links), and builds an interactive 3D/2D
Force Graph using Vis-network / Force-Graph for GitHub Pages static site deployment.

Usage:
    python3 scripts/build_knowledge_graph.py [--output docs/graph.html]
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

from lib_content import REPO_ROOT, all_questions, load_topics

LINK_RE = re.compile(r"\[[^\]]*\]\((\.[^)\s]+)\)")
WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")

DIFFICULTY_COLORS = {
    "Beginner": "#22c55e",      # Green
    "Intermediate": "#eab308",  # Yellow
    "Advanced": "#ef4444",      # Red
    "Topic": "#8b5cf6",         # Purple
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

    nodes = []
    edges = []
    edge_set = set()

    # 1. Add Topic Nodes
    for t in topics:
        nodes.append({
            "id": f"topic:{t.directory}",
            "label": t.title,
            "group": "Topic",
            "val": 15,
            "color": DIFFICULTY_COLORS["Topic"],
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
        topic_node_id = f"topic:{q.path.parent.name}"

        nodes.append({
            "id": node_id,
            "label": f"#{q.id} {q.title}",
            "title": q.title,
            "group": q.difficulty,
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
                "color": "rgba(139, 92, 246, 0.3)"
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
                        "color": "rgba(59, 130, 246, 0.5)"
                    })

    # 4. Connect Questions sharing identical specific tags (Tag Similarity Edges)
    tag_map: dict[str, list[str]] = {}
    for q in questions:
        for tag in q.tags:
            if tag in {"ai-engineering", "interview-questions"}:
                continue # Skip generic tags
            tag_map.setdefault(tag, []).append(f"q:{q.id}")

    for tag, q_ids in tag_map.items():
        if len(q_ids) > 1 and len(q_ids) <= 6: # Connect closely related tagged items
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
                            "color": "rgba(234, 179, 8, 0.15)"
                        })

    return {"nodes": nodes, "links": edges}


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI Engineering Knowledge Graph</title>
  <script src="https://unpkg.com/3d-force-graph"></script>
  <script src="https://unpkg.com/three"></script>
  <style>
    body {{
      margin: 0;
      padding: 0;
      background-color: #030712;
      color: #f8fafc;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      overflow: hidden;
    }}
    #header {{
      position: absolute;
      top: 15px;
      left: 20px;
      z-index: 10;
      background: rgba(15, 23, 42, 0.85);
      padding: 15px 20px;
      border-radius: 12px;
      border: 1px solid #334155;
      backdrop-filter: blur(8px);
      max-width: 360px;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }}
    h1 {{
      margin: 0 0 6px 0;
      font-size: 1.2rem;
      color: #38bdf8;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    p {{
      margin: 0 0 10px 0;
      font-size: 0.85rem;
      color: #94a3b8;
      line-height: 1.4;
    }}
    .legend {{
      display: flex;
      gap: 12px;
      font-size: 0.8rem;
      flex-wrap: wrap;
      margin-top: 8px;
    }}
    .legend-item {{
      display: flex;
      align-items: center;
      gap: 5px;
    }}
    .dot {{
      width: 10px;
      height: 10px;
      border-radius: 50%;
      display: inline-block;
    }}
    #graph {{
      width: 100vw;
      height: 100vh;
    }}
    #info-card {{
      position: absolute;
      bottom: 20px;
      right: 20px;
      z-index: 10;
      background: rgba(15, 23, 42, 0.9);
      padding: 16px 20px;
      border-radius: 12px;
      border: 1px solid #334155;
      display: none;
      max-width: 340px;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
      backdrop-filter: blur(8px);
    }}
    #info-card h3 {{
      margin: 0 0 8px 0;
      font-size: 1.05rem;
      color: #f1f5f9;
    }}
    #info-card p {{
      margin: 0 0 12px 0;
      color: #cbd5e1;
      white-space: pre-line;
    }}
    #info-card a {{
      display: inline-block;
      background: #0284c7;
      color: #ffffff;
      padding: 6px 12px;
      border-radius: 6px;
      text-decoration: none;
      font-size: 0.85rem;
      font-weight: 500;
      transition: background 0.2s ease;
    }}
    #info-card a:hover {{
      background: #0369a1;
    }}
  </style>
</head>
<body>
  <div id="header">
    <h1>🌐 3D AI Engineering Knowledge Graph</h1>
    <p>Interactive 3D network visualizing 200 questions, 10 topics, and cross-topic concept wikilinks.</p>
    <div class="legend">
      <div class="legend-item"><span class="dot" style="background:#8b5cf6"></span> Topic Node</div>
      <div class="legend-item"><span class="dot" style="background:#22c55e"></span> Beginner</div>
      <div class="legend-item"><span class="dot" style="background:#eab308"></span> Intermediate</div>
      <div class="legend-item"><span class="dot" style="background:#ef4444"></span> Advanced</div>
    </div>
  </div>

  <div id="info-card">
    <h3 id="card-title">Node Info</h3>
    <p id="card-desc"></p>
    <a id="card-link" href="#" target="_blank">Open Markdown Source File →</a>
  </div>

  <div id="graph"></div>

  <script>
    const gData = {graph_json};

    const card = document.getElementById('info-card');
    const cardTitle = document.getElementById('card-title');
    const cardDesc = document.getElementById('card-desc');
    const cardLink = document.getElementById('card-link');

    const Graph = ForceGraph3D()
      (document.getElementById('graph'))
        .graphData(gData)
        .nodeId('id')
        .nodeVal('val')
        .nodeColor('color')
        .nodeLabel('label')
        .nodeResolution(16)
        .linkOpacity(0.35)
        .linkWidth(link => link.type === 'topic-link' ? 1.8 : 0.8)
        .linkColor(link => link.color || 'rgba(148, 163, 184, 0.25)')
        .linkDirectionalParticles(link => link.type === 'cross-link' ? 3 : 0)
        .linkDirectionalParticleWidth(2.0)
        .linkDirectionalParticleSpeed(0.006)
        .onNodeHover(node => {{
          document.body.style.cursor = node ? 'pointer' : 'default';
        }})
        .onNodeClick(node => {{
          if (node) {{
            // Aim camera at node
            const distance = 120;
            const distRatio = 1 + distance/Math.hypot(node.x, node.y, node.z);
            Graph.cameraPosition(
              {{ x: node.x * distRatio, y: node.y * distRatio, z: node.z * distRatio }},
              node, // lookAt ({x, y, z})
              2000  // transition duration ms
            );

            cardTitle.innerText = node.label;
            cardDesc.innerText = `Category: ${{node.category || 'Topic Hub'}}\nDifficulty: ${{node.group || node.type}}\nType: ${{node.type}}`;
            cardLink.href = `https://github.com/mchittineni/ultimate-ai-engineering-guide/blob/main/${{node.url.replace('./', '')}}`;
            card.style.display = 'block';
          }}
        }});

    // Add ambient background rotation
    Graph.d3Force('charge').strength(-120);
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

    html_content = HTML_TEMPLATE.format(graph_json=json.dumps(graph_data, indent=2))
    output_path.write_text(html_content, encoding="utf-8")

    print(f"Successfully generated Knowledge Graph at: {output_path}")
    print(f"Nodes: {len(graph_data['nodes'])}, Edges: {len(graph_data['links'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
