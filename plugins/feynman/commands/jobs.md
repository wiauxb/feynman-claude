---
description: Inspect visible research run state, scheduled research follow-ups when available, and durable watch artifacts.
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

Inspect active research work for this project.

Requirements:
- Use the `process` tool with the `list` action only when that tool is visible and the user is asking about research-run state; otherwise record `Process state: BLOCKED - process tool not available`.
- Use scheduling tooling only when it is visible; otherwise record `Schedule state: BLOCKED - scheduling tool not available`.
- Inspect durable state in `outputs/.plans/`, `outputs/`, `experiments/`, and `notes/` for watch baselines, autoresearch logs, replication runs, and recent research artifacts.
- Summarize:
  - active research-run background processes if the process tool is visible
  - queued or recurring research watches if scheduling tooling is visible
  - durable watch/autoresearch/replication artifacts found on disk
  - failures that need attention
  - the next concrete command the user should run if they want logs or detailed status
- Be concise and operational.
