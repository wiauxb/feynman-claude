---
description: Create a research watch baseline with an optional scheduled follow-up when scheduling tools are visible.
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

Create a research watch baseline for: $ARGUMENTS

Derive a short slug from the watch topic (lowercase, hyphens, no filler words, ≤5 words). Use this slug for all files in this run.

Requirements:
- Before starting, outline the watch plan: what to monitor, what signals matter, what counts as a meaningful change, and the requested or sensible check frequency. Write the plan to `outputs/.plans/<slug>.md`. Briefly summarize the plan to the user and continue immediately. Do not ask for confirmation or wait for a proceed response unless the user explicitly requested plan review.
- Start with a baseline sweep of the topic.
- Use an external cron job to create the recurring or delayed follow-up only when that tool is visible in the current tool set.
- If an external cron job is not visible, do not claim a recurring watch was scheduled. Record `Scheduling: BLOCKED - schedule_prompt not available` in the plan and baseline artifact, then give the exact command or prompt the user can run later to refresh the watch.
- Save exactly one baseline artifact to `outputs/<slug>-baseline.md`.
- End with a `Sources` section containing direct URLs for every source used.
