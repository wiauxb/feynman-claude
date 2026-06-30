---
description: Compare multiple sources on a topic and produce a source-grounded matrix of agreements, disagreements, and confidence.
argument-hint: <topic>
---

## Tool Discipline (Read First)

Tool names are literal. Use only tools visible in the current tool set.

- Search the web with the `WebSearch` tool.
- Read URLs with the `WebFetch` tool.
- Use the alphaXiv MCP tools (`mcp__alphaxiv__discover_papers`, `mcp__alphaxiv__get_paper_content`, `mcp__alphaxiv__answer_pdf_queries`, `mcp__alphaxiv__read_files_from_github_repository`) for academic paper search, reading, Q&A, and repository inspection. If the alphaXiv MCP is unavailable, the `alpha` CLI via `Bash` (`alpha search|get|ask|code`, after `alpha login`) is a fallback.
- To ask the user a question, write plain chat text and wait for the next user message.
- Delegate to subagents with the `Task` tool, setting `subagent_type` to `feynman-researcher`, `feynman-verifier`, or `feynman-reviewer`.
- If a tool returns `Tool not found` or `Invalid URL`, do not retry the same invalid call. Map to a canonical visible tool and valid arguments, or record the capability as blocked.

Compare sources for: $ARGUMENTS

Derive a short slug from the comparison topic (lowercase, hyphens, no filler words, ≤5 words). Use this slug for all files in this run.

Requirements:
- Before starting, outline the comparison plan: which sources to compare, which dimensions to evaluate, expected output structure. Write the plan to `outputs/.plans/<slug>.md`. Briefly summarize the plan to the user and continue immediately. Do not ask for confirmation or wait for a proceed response unless the user explicitly requested plan review.
- Use the `feynman-researcher` subagent to gather source material when the comparison set is broad, and the `feynman-verifier` subagent to verify sources and add inline citations to the final matrix.
- Build a comparison matrix covering: source, key claim, evidence type, caveats, confidence.
- Generate charts only when a chart tool is visible and the comparison involves quantitative metrics; otherwise include a source-backed table or chart specification. Use Mermaid for method or architecture comparisons when the structure is source-supported.
- Distinguish agreement, disagreement, and uncertainty clearly.
- Save exactly one comparison to `outputs/<slug>-comparison.md`.
- End with a `Sources` section containing direct URLs for every source used.
