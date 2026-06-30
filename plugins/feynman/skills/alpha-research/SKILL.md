---
name: alpha-research
description: Search, read, and query research papers via the alphaXiv MCP tools. Use when the user asks about academic papers, wants to find research on a topic, needs to read a specific paper, ask questions about a paper, inspect a paper's code repository, or manage paper annotations.
---

# Alpha Research CLI

Use the alphaXiv MCP tools when they are available. For shell commands, use `alpha ...` as a fallback.

## Commands

| Command | Description |
|---------|-------------|
| `alpha search "<query>"` | Search papers. Prefer `--mode semantic` by default; use `--mode keyword` only for exact-term lookup and `--mode agentic` for broader retrieval. |
| `alpha get <arxiv-id-or-url>` | Fetch paper content and any local annotation |
| `alpha get --full-text <arxiv-id>` | Get raw full text instead of AI report |
| `alpha ask <arxiv-id> "<question>"` | Ask a question about a paper's PDF |
| `alpha code <github-url> [path]` | Read files from a paper's GitHub repo. Use `/` for overview |
| `alpha annotate <paper-id> "<note>"` | Save a persistent annotation on a paper |
| `alpha annotate --clear <paper-id>` | Remove an annotation |
| `alpha annotate --list` | List all annotations |

## Auth

Run `alpha login` to authenticate with alphaXiv. Check status with `alpha status`.

## Examples

```bash
alpha search "transformer scaling laws"
alpha search --mode agentic "efficient attention mechanisms for long context"
alpha get 2106.09685
alpha ask 2106.09685 "What optimizer did they use?"
alpha code https://github.com/karpathy/nanoGPT src/model.py
alpha annotate 2106.09685 "Key paper on LoRA - revisit for adapter comparison"
```

## When to use

- Academic paper search, reading, Q&A → Feynman alpha tools or `feynman alpha`
- Current topics (products, releases, docs) → web search tools
- Mixed topics → combine both
