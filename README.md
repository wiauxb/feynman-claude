# Feynman for Claude Code

A port of the [Feynman](https://www.feynman.is/) research agent to **Claude Code**, packaged as a
plugin. It brings Feynman's deep-research workflow — plan → gather (parallel subagents) → draft →
cite → adversarial review → deliver, with provenance — to Claude Code, backed by the **alphaXiv MCP**
for academic paper search. No Anthropic API key required: it runs on your Claude Code subscription.

Generated from upstream `companion-inc/feynman` (a pinned git submodule) by `generate.py`, which
rewrites Pi-runtime tools to Claude Code tools + the alphaXiv MCP.

## What you get

- **13 commands** — `/feynman:deepresearch`, `/feynman:lit`, `/feynman:review`, `/feynman:audit`,
  `/feynman:compare`, `/feynman:replicate`, `/feynman:draft`, `/feynman:recipe`, `/feynman:summarize`,
  `/feynman:autoresearch`, `/feynman:watch`, `/feynman:log`, `/feynman:jobs`.
- **5 agents** — `feynman` (lead) + `feynman-researcher`, `feynman-verifier`, `feynman-reviewer`,
  `feynman-writer` subagents.
- **20 skills** — auto-triggering research capabilities (deep-research, literature-review, paper-writing,
  peer-review, paper-code-audit, source-comparison, replication, alpha-research, …).
- The **alphaXiv MCP** (`https://api.alphaxiv.org/mcp/v1`), declared in the plugin so it auto-registers
  on install.

## Install

Add the marketplace, then install at the scope you want. **The project-vs-global choice is made here at
install time** — there is no separate installer.

```
/plugin marketplace add wiauxb/feynman-claude            # this repo
/plugin install feynman@feynman-claude --scope project   # this project only
/plugin install feynman@feynman-claude --scope user      # all your projects (global)
/plugin install feynman@feynman-claude --scope local     # this project, private (gitignored)
```

Then **authenticate the alphaXiv MCP once** (see below), and restart Claude Code so the plugin loads.

### Authenticate the alphaXiv MCP (one-time, free account)

The plugin declares the alphaXiv MCP. On first connect, Claude Code runs an OAuth flow to your free
alphaXiv account. **Known snag:** Claude Code requests the `offline_access` scope, which alphaXiv
rejects (`invalid_scope`). Work around it:

1. Run `/mcp` → select **alphaxiv** → **Authenticate**. If it errors with `invalid_scope: offline_access`,
   copy the authorization URL it produced.
2. Re-open that URL with `&scope=email+profile` (delete `+offline_access` from the `scope=` parameter),
   and approve in the browser.
3. The localhost callback completes the flow; `/mcp` then shows **alphaxiv → connected**.

This is an alphaXiv-account login only — unrelated to any Anthropic API access.

### Fallback: the `alpha` CLI

If you'd rather not use the MCP (or it's unavailable), the workflows fall back to the `alpha` CLI:

```
npm i -g @companion-ai/alpha-hub
alpha login
```

The research agents use `alpha search|get|ask|code` via Bash when the MCP isn't present.

### No marketplace? Directory fallback

To use it in one project without a marketplace, copy the plugin into the project's skills dir:

```
cp -r plugins/feynman/agents plugins/feynman/commands plugins/feynman/skills /path/to/project/.claude
```

It auto-loads (after the workspace-trust prompt). Add the alphaXiv MCP manually:
`claude mcp add --transport http alphaxiv https://api.alphaxiv.org/mcp/v1`.

## Updating from upstream (deliberate, never automatic)

I will update this repo from time to time, but if you cannot wait to get the fresh upstream updates,
you can follow the here-under instructions.

The upstream Feynman is a **frozen submodule** — the recorded commit SHA is the freeze. To take a new
upstream version:

```
cd feynman && git fetch origin && git checkout <reviewed-commit> && cd ..
git add feynman                 # re-pin the gitlink to the reviewed commit
python3 generate.py             # regenerate commands/agents/skills
```

Never `git submodule update --remote` blindly — review the upstream diff first. The plugin-wrapper
files (`.claude-plugin/plugin.json`, `.mcp.json`, this README, the root `marketplace.json`) are static
and are not touched by `generate.py`.

## How the port works

`generate.py` reads the submodule's `prompts/`, `skills/`, `.feynman/agents/`, and `.feynman/SYSTEM.md`
and applies three rewrite layers:

1. **Block rewrites** — hand-audited replacements for the "Tool Discipline" / do-not-call blocks that
   upstream uses to forbid the very tools Claude Code needs (`WebSearch`/`WebFetch`/`Task`), plus the
   `alpha`-CLI and `subagent`-dispatch prose.
2. **Tool map** — token-level Pi → Claude Code / alphaXiv MCP tool-name substitutions.
3. **Phrase rewrites** — make the alphaXiv MCP the primary paper backend and the `alpha` CLI the fallback.

Prompts become `/feynman:*` commands; `.feynman/agents/*` become `feynman-*` subagents; `SYSTEM.md`
becomes the `feynman` lead agent; skills are carried over and re-pointed at the MCP.

## Credits & License

MIT. Upstream research agent: [companion-inc/feynman](https://github.com/companion-inc/feynman).
Generator approach forked from [Maverobot/feynman-copilot](https://github.com/Maverobot/feynman-copilot)
(GitHub Copilot CLI port) and retargeted to Claude Code + the alphaXiv MCP.
