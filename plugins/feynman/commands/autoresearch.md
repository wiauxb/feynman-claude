---
description: Bounded research experiment loop - try hypotheses, measure benchmark evidence, keep what works, discard what doesn't, repeat.
argument-hint: <idea>
---

## Tool Discipline (Read First)

Tool names are literal. Use only tools visible in the current tool set.

- Search the web with the `WebSearch` tool.
- Read URLs with the `WebFetch` tool.
- Use the alphaXiv MCP tools (`mcp__alphaxiv__discover_papers`, `mcp__alphaxiv__get_paper_content`, `mcp__alphaxiv__answer_pdf_queries`, `mcp__alphaxiv__read_files_from_github_repository`) for academic paper search, reading, Q&A, and repository inspection. If the alphaXiv MCP is unavailable, the `alpha` CLI via `Bash` (`alpha search|get|ask|code`, after `alpha login`) is a fallback.
- To ask the user a question, write plain chat text and wait for the next user message.
- Delegate to subagents with the `Task` tool, setting `subagent_type` to `feynman-researcher`, `feynman-verifier`, or `feynman-reviewer`.
- If a tool returns `Tool not found` or `Invalid URL`, do not retry the same invalid call. Map to a canonical visible tool and valid arguments, or record the capability as blocked.

Start an autoresearch optimization loop for: $ARGUMENTS

This command runs a bounded foreground research experiment loop using the visible tools in this session.

## Step 1: Gather

If `autoresearch.md` and `autoresearch.jsonl` already exist, ask the user if they want to resume or start fresh.
If `CHANGELOG.md` exists, read the most recent relevant entries before resuming.

Otherwise, collect the following from the user before doing anything else:
- What to optimize (model accuracy, retrieval quality, training loss, ablation score, evaluation latency, etc.)
- The benchmark command to run
- The metric name, unit, and direction (lower/higher is better)
- Files in scope for changes
- Maximum number of iterations (default: 20)

## Step 2: Environment

Ask the user where to run:
- **Local** — run in the current working directory
- **New git branch** — create a branch so main stays clean
- **Virtual environment** — create an isolated venv/conda env first
- **Docker** — run experiment code inside an isolated Docker container
- **Modal** — run on Modal's serverless GPU infrastructure. Write Modal-decorated scripts and execute with `modal run`. Best for GPU-heavy benchmarks with no persistent state between iterations. Requires `modal` CLI.
- **RunPod** — provision a GPU pod via `runpodctl` and run iterations there over SSH. Best for experiments needing persistent state, large datasets, or SSH access between iterations. Requires `runpodctl` CLI.

Do not proceed without a clear answer.

## Step 3: Confirm

Present the full plan to the user before starting:

```
Optimization target: [metric] ([direction])
Benchmark command:   [command]
Files in scope:      [files]
Environment:         [chosen environment]
Max iterations:      [N]
```

Ask the user to confirm. Do not start the loop without explicit approval.

## Step 4: Run

Initialize the session: create `autoresearch.md`, `autoresearch.jsonl`, `autoresearch.sh`, run the baseline, and start looping.

Each iteration: edit -> run the benchmark -> log the benchmark result, evidence, and decision -> compare against the baseline -> keep the change, revert it, or record the failed hypothesis -> repeat. Do not stop unless interrupted or `maxIterations` is reached.
After the baseline and after meaningful iteration milestones, append a concise entry to `CHANGELOG.md` summarizing what changed, what metric result was observed, what failed, and the next step.

## Optional tools

Use these only when they are visible in the current tool set:

- Bash - one-time session config (name, metric, unit, direction)
- Bash - run the benchmark command, capture output and wall-clock time
- Bash - record the benchmark result, evidence, and decision in the autoresearch log

## Subcommands

- `/autoresearch <text>` — start or resume the loop
- `/autoresearch off` — stop the loop, keep data
- `/autoresearch clear` — delete all state and start fresh
