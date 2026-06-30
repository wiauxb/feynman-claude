---
description: Run an internal research critique with likely objections, severity, and a concrete revision plan.
argument-hint: <artifact>
---

## Tool Discipline (Read First)

Tool names are literal. Use only tools visible in the current tool set.

- Search the web with the `WebSearch` tool.
- Read URLs with the `WebFetch` tool.
- Use the alphaXiv MCP tools (`mcp__alphaxiv__discover_papers`, `mcp__alphaxiv__get_paper_content`, `mcp__alphaxiv__answer_pdf_queries`, `mcp__alphaxiv__read_files_from_github_repository`) for academic paper search, reading, Q&A, and repository inspection. If the alphaXiv MCP is unavailable, the `alpha` CLI via `Bash` (`alpha search|get|ask|code`, after `alpha login`) is a fallback.
- To ask the user a question, write plain chat text and wait for the next user message.
- Delegate to subagents with the `Task` tool, setting `subagent_type` to `feynman-researcher`, `feynman-verifier`, or `feynman-reviewer`.
- If a tool returns `Tool not found` or `Invalid URL`, do not retry the same invalid call. Map to a canonical visible tool and valid arguments, or record the capability as blocked.

Review this AI research artifact: $ARGUMENTS

Derive a short slug from the artifact name (lowercase, hyphens, no filler words, ≤5 words). Use this slug for all files in this run.

This is an execution request, not a request to explain or implement the workflow instructions. Carry out the workflow with tools and durable files. Do not answer by describing the protocol, saying what you would do, or stopping after a plan.

Do not ask for confirmation. Briefly summarize the plan to the user and continue immediately unless the user explicitly asked to review the plan first.

Required artifacts:
- Plan: `outputs/.plans/<slug>-review-plan.md`
- Evidence notes: `outputs/.drafts/<slug>-review-evidence.md`
- Final review: `outputs/<slug>-review.md`

Workflow:
1. Create `outputs/.plans`, `outputs/.drafts`, and `outputs`.
2. Write `outputs/.plans/<slug>-review-plan.md` with:
   - artifact identifier and source type (arXiv ID, URL, local file, PDF, Markdown, etc.)
   - review criteria: novelty, empirical rigor, baselines, reproducibility, claims validity, figures/tables, metrics, related work, writing quality
   - verification checks needed for claims, figures, reported metrics, data/code availability, and linked artifacts
3. Continue immediately. Do not end after planning.
4. Inspect the artifact:
   - For local files, read or parse the file directly.
   - For PDFs, use available PDF/document parsing tools. If PDF parsing fails, use any available fallback extraction, record the failure, and still produce a blocked or partial review artifact.
   - For arXiv IDs or URLs, fetch the paper/source directly and record the URL.
   - Inspect linked code, datasets, supplemental material, or citations when they are reachable and materially affect the review.
5. Write evidence notes to `outputs/.drafts/<slug>-review-evidence.md` before writing the final review. Include quoted/paraphrased claims, observed methods, reported metrics, baseline comparisons, reproducibility facts, and every inspected source path or URL.
6. Use the `feynman-researcher` and `feynman-reviewer` subagents only if the `Task` tool is available and the artifact is large enough to benefit from delegation. If subagents are unavailable, fail, or would only add overhead, do the lead-owned review directly. Never merely say a subagent was spawned; either call the tool or continue yourself.
7. Write exactly one final review artifact to `outputs/<slug>-review.md` with:
   - Summary Assessment
   - Strengths
   - Critical Issues
   - Major Issues
   - Minor Issues
   - Reproducibility and Verification
   - Inline Annotations tied to sections, claims, figures, or tables where possible
   - Recommendation
   - Sources
8. If the artifact cannot be parsed or critical evidence is unavailable, still write `outputs/<slug>-review.md`. Mark the affected sections with `Verification: BLOCKED`, explain exactly what failed, and distinguish blocked checks from actual paper weaknesses.
9. Before responding, verify on disk that `outputs/<slug>-review.md` exists. If it does not exist, create it immediately as a blocked review artifact with the failure reason.

Never end with planning-only chat. Never ask what to do next. Never claim the review is complete unless `outputs/<slug>-review.md` exists.
