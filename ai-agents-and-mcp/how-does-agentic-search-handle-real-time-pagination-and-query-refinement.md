---
title: "How does Agentic Search handle real-time pagination and query refinement?"
id: 137
category: "AI Agents and MCP"
difficulty: "Intermediate"
tags:
  - ai-engineering
  - ai-agents-and-mcp
  - interview-questions
---

# How does Agentic Search handle real-time pagination and query refinement?

**Short answer:** Agentic Search replaces single-shot search engine queries with multi-turn agentic loops, allowing an LLM to evaluate search snippet relevance, issue refined follow-up search queries, handle pagination, and open specific web page links until target information is fully retrieved.

## Detail

Single-shot RAG fails when initial web search results return generic marketing text or fragmented snippets.

```text
[Initial Query "NVIDIA Q3 revenue"] ──► Web Search ──► Returns Generic Marketing Snippets
                                                             │
                                                             ▼
[Agent Evaluates Snippets] ──► Query Refinement: "NVIDIA Q3 2024 earnings release 10-Q filing pdf"
                                                             │
                                                             ▼
[Page Reader Tool] ◄── Pagination / Link Selection ◄── Targeted Web Search
```

### Agentic Search Execution Mechanics

1. **Initial Broad Search:** Issue preliminary search query.
2. **Relevance Critique:** Inspect returned title/snippet lists.
3. **Targeted Deep Dive:** Execute specific sub-tools: `click_link(url)`, `paginate_results(page=2)`, or `refine_query(new_query)`.
4. **Context Synthesis:** Extract exact text paragraphs into agent memory.

## Example

Python concept illustrating agent query refinement logic:

```python
def agentic_search_step(current_results: list[dict], search_tool, query_refiner_fn) -> str:
    # Check if current snippets contain target metric
    has_answer = any("revenue" in r["snippet"].lower() for r in current_results)

    if not has_answer:
        # Refine search query with specialized keywords
        refined_query = query_refiner_fn("NVIDIA financial Q3 SEC filing 10-Q")
        new_results = search_tool(refined_query)
        return f"Refined search issued: '{refined_query}'. Found {len(new_results)} new matches."

    return "Target information located in current snippets."
```

## Interview tips

- Discuss web scraping rate limits, domain blocking, and HTML-to-Markdown conversion (using tools like Tavily, Perplexity API, or Firecrawl).
- Highlight preventing infinite web browsing loops via step budgets and link extraction caps.

## Related Concepts

- [[How does Reciprocal Rank Fusion (RRF) combine scores from sparse and dense retrievers?]] (`#127`): [How does Reciprocal Rank Fusion (RRF) combine scores from sparse and dense retrievers?](../rag-and-vector-databases/how-does-reciprocal-rank-fusion-rrf-combine-scores-from-sparse-and-dense-retrievers.md)
- [[What is indirect prompt injection and how does it occur when parsing web pages/documents?]] (`#181`): [What is indirect prompt injection and how does it occur when parsing web pages/documents?](../ai-safety-and-governance/what-is-indirect-prompt-injection-and-how-does-it-occur-when-parsing-web-pages-documents.md)
- [[How to conduct a complete system design interview for a multi-tenant enterprise RAG search platform?]] (`#199`): [How to conduct a complete system design interview for a multi-tenant enterprise RAG search platform?](../interview-experience/how-to-conduct-a-complete-system-design-interview-for-a-multi-tenant-enterprise-rag-search-platform.md)

---

[⬅ Back to AI Agents and MCP](./README.md) · [All topics](../README.md)
