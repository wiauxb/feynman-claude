---
description: Plan a replication workflow for a paper, claim, or benchmark; execute only after an explicit environment choice.
argument-hint: <paper>
---

## Tool Discipline (Read First)

Tool names are literal. Use only tools visible in the current tool set.

- Search the web with the `WebSearch` tool.
- Read URLs with the `WebFetch` tool.
- Use the alphaXiv MCP tools (`mcp__alphaxiv__discover_papers`, `mcp__alphaxiv__get_paper_content`, `mcp__alphaxiv__answer_pdf_queries`, `mcp__alphaxiv__read_files_from_github_repository`) for academic paper search, reading, Q&A, and repository inspection. If the alphaXiv MCP is unavailable, the `alpha` CLI via `Bash` (`alpha search|get|ask|code`, after `alpha login`) is a fallback.
- To ask the user a question, write plain chat text and wait for the next user message.
- Delegate to subagents with the `Task` tool, setting `subagent_type` to `feynman-researcher`, `feynman-verifier`, or `feynman-reviewer`.
- If a tool returns `Tool not found` or `Invalid URL`, do not retry the same invalid call. Map to a canonical visible tool and valid arguments, or record the capability as blocked.

Design a replication plan for: $ARGUMENTS

## Workflow

1. **Extract** — Use the `feynman-researcher` subagent to pull implementation details from the target paper and any linked code. If `CHANGELOG.md` exists, read the most recent relevant entries before planning or resuming.
2. **Recipe pass** — For ML training, fine-tuning, benchmark, or dataset-heavy targets, perform a recipe extraction before execution planning. Link each claimed result to the exact dataset, method, hyperparameters, compute assumptions, metric, and code path that produced it. Validate dataset availability/schema when possible and mark unchecked details as `unverified` instead of assuming they are usable.
3. **Plan** — Determine what code, datasets, metrics, and environment are needed. Be explicit about what is verified, what is inferred, what is still missing, and which checks or test oracles will be used to decide whether the replication succeeded.
4. **Environment** — Before running anything, ask the user where to execute:
   - **Local** — run in the current working directory
   - **Virtual environment** — create an isolated venv/conda env first
   - **Docker** — run experiment code inside an isolated Docker container
   - **Modal** — run on Modal's serverless GPU infrastructure. Write a Modal-decorated Python script and execute with `modal run <script.py>`. Best for burst GPU jobs that don't need persistent state. Requires `modal` CLI (`pip install modal && modal setup`).
   - **RunPod** — provision a GPU pod on RunPod and SSH in for execution. Use `runpodctl` to create pods, transfer files, and manage lifecycle. Best for long-running experiments or when you need SSH access and persistent storage. Requires `runpodctl` CLI and `RUNPOD_API_KEY`.
   - **Plan only** — produce the replication plan without executing
5. **Execute** — If the user chose an execution environment, implement and run the replication steps there. Save notes, scripts, raw outputs, and results to disk in a reproducible layout. Do not call the outcome replicated unless the planned checks actually passed.
6. **Log** — For multi-step or resumable replication work, append concise entries to `CHANGELOG.md` after meaningful progress, failed attempts, major verification outcomes, and before stopping. Record the active objective, what changed, what was checked, and the next step.
7. **Report** — End with a `Sources` section containing paper, dataset, documentation, and repository URLs.

Do not install packages, run training, or execute experiments without confirming the execution environment first.
