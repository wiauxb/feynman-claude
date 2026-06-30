---
description: Find ranked, implementable ML training recipes backed by papers, datasets, docs, and code.
argument-hint: <task-or-paper>
---

## Tool Discipline (Read First)

Tool names are literal. Use only tools visible in the current tool set.

- Search the web with the `WebSearch` tool.
- Read URLs with the `WebFetch` tool.
- Use the alphaXiv MCP tools (`mcp__alphaxiv__discover_papers`, `mcp__alphaxiv__get_paper_content`, `mcp__alphaxiv__answer_pdf_queries`, `mcp__alphaxiv__read_files_from_github_repository`) for academic paper search, reading, Q&A, and repository inspection. If the alphaXiv MCP is unavailable, the `alpha` CLI via `Bash` (`alpha search|get|ask|code`, after `alpha login`) is a fallback.
- To ask the user a question, write plain chat text and wait for the next user message.
- Delegate to subagents with the `Task` tool, setting `subagent_type` to `feynman-researcher`, `feynman-verifier`, or `feynman-reviewer`.
- If a tool returns `Tool not found` or `Invalid URL`, do not retry the same invalid call. Map to a canonical visible tool and valid arguments, or record the capability as blocked.

Find implementable ML training recipes for: $ARGUMENTS

Derive a short slug from the task (lowercase, hyphens, no filler words, ≤5 words). Use this slug for all files in this run.

This is an execution request, not a request to explain the workflow. Continue immediately.

## Required artifacts

- `outputs/.plans/<slug>-recipe.md`
- `outputs/.drafts/<slug>-recipe-research.md`
- `outputs/<slug>-recipe.md`
- `outputs/<slug>-recipe.provenance.md`

## Workflow

1. **Plan** — Write `outputs/.plans/<slug>-recipe.md` with the target task, benchmark or desired behavior, candidate source types, feasibility constraints, and a task ledger. Continue automatically after writing the plan.
2. **Research** — Use the `feynman-researcher` subagent when the task needs a broad paper/code sweep. For narrow tasks, gather evidence directly. The research must start from evidence of results, not from example scripts alone.
3. **Recipe extraction** — For each promising approach, link the observed result to the exact recipe that produced it. A useful entry has: paper or report, benchmark/result, dataset, training method, key hyperparameters, compute assumptions, implementation code path, and current docs.
4. **Dataset validation** — Check whether each dataset is available, what splits/columns it exposes, and whether the format matches the method. Use WebFetch on the dataset card for Hugging Face datasets when available. If schema or availability was not directly checked, mark it `unverified`; do not imply it is usable.
5. **Implementation grounding** — Find working code or official docs for the chosen training path. Use WebFetch on the repo and WebFetch on the file for relevant Hugging Face Hub repos. Prefer current official docs and actively maintained repos. Record exact file paths, function names, class names, and command patterns when available.
6. **Synthesis** — Write `outputs/.drafts/<slug>-recipe-research.md` first, then promote a concise final ranked brief to `outputs/<slug>-recipe.md`.
7. **Verification** — For any recipe you rank first, verify the key source URLs and the dataset/code availability before final delivery. If a source, dataset, or code path cannot be checked, keep it in the brief only with an explicit `blocked` or `unverified` label.
8. **Provenance** — Write `outputs/<slug>-recipe.provenance.md` with date, sources consulted, sources accepted/rejected, verification status, and artifact paths.

## Required final shape

The final brief must include:

- **Recommendation:** the one recipe to try first and why.
- **Ranked recipe table:** one row per candidate with paper/source, result, dataset, method, hyperparameters, compute, code/docs, and verification status.
- **Dataset notes:** schema, split, size, license/access constraints when checked.
- **Implementation plan:** minimal steps to run the top recipe.
- **Known gaps:** missing code, inaccessible data, unclear hyperparameters, or benchmark mismatch.
- **Sources:** URLs for every paper, repo, dataset, and doc page used.

Do not claim a method is state of the art, replicated, or production-ready unless the underlying checks prove it. Use `verified`, `unverified`, `blocked`, and `inferred` precisely.
