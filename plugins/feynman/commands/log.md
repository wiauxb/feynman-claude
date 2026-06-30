---
description: Write a durable session log with completed work, findings, open questions, and next steps.
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

Write a session log for the current research work.

Requirements:
- Summarize what was done in this session.
- Capture the strongest findings or decisions.
- List open questions, unresolved risks, and concrete next steps.
- Reference any important artifacts written to `notes/`, `outputs/`, `experiments/`, or `papers/`.
- If any external claims matter, include direct source URLs.
- Save the log to `notes/` as markdown with a date-oriented filename.
