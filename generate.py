#!/usr/bin/env python3
"""Generate Claude Code-compatible commands, skills, and agents from the feynman submodule.

Reads the upstream feynman repo (skills, prompts, .feynman/agents, .feynman/SYSTEM.md) and
produces Claude Code assets under plugins/feynman/ with Pi-specific tool references replaced by
Claude Code equivalents and the alphaXiv MCP:

    prompts/*.md            -> commands/feynman/*.md   (slash commands: /feynman:<name>)
    skills/<name>/SKILL.md   -> skills/<name>/SKILL.md  (thin trigger skills, all of them)
    .feynman/agents/*.md     -> agents/feynman-*.md     (subagents)
    .feynman/SYSTEM.md       -> agents/feynman.md        (lead research agent)

Two-layer rewrite:
  1. BLOCK_REWRITES — hand-audited replacements for "Tool Discipline" / do-not-call blocks and
     alpha-CLI / subagent-dispatch prose that a naive token swap would corrupt (e.g. upstream
     literally forbids WebSearch/WebFetch/Task — the tools we now require).
  2. TOOL_MAP — token-level Pi->Claude/MCP tool-name substitutions for everything else.

Usage:
    python3 generate.py              # default: feynman submodule at ./feynman
    python3 generate.py /path/to/feynman
"""

import re
import sys
import shutil
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

FEYNMAN_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "feynman"
OUTPUT_DIR = Path(__file__).parent / "plugins" / "feynman"
# Flat commands/ — as a plugin named "feynman", commands resolve to /feynman:<name>; a nested
# commands/feynman/ subdir would double the namespace to /feynman:feynman:<name>.
COMMANDS_OUT = OUTPUT_DIR / "commands"
SKILLS_OUT = OUTPUT_DIR / "skills"
AGENTS_OUT = OUTPUT_DIR / "agents"
# Static plugin-wrapper files (plugin.json, .mcp.json, root marketplace.json, README) are NOT
# generated — they live in version control and survive regeneration (which only rewrites
# commands/skills/agents from the submodule).

# The four research subagents are exposed as feynman-<name>; tool lists are curated to match the
# validated hand-port (loose .claude/ golden). Subagent tools must be listed explicitly in Claude.
AGENT_TOOLS = {
    "researcher": "Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, "
                  "mcp__alphaxiv__discover_papers, mcp__alphaxiv__get_paper_content, "
                  "mcp__alphaxiv__answer_pdf_queries, mcp__alphaxiv__read_files_from_github_repository",
    "verifier":  "Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, "
                 "mcp__alphaxiv__get_paper_content, mcp__alphaxiv__answer_pdf_queries",
    "reviewer":  "Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, "
                 "mcp__alphaxiv__get_paper_content, mcp__alphaxiv__answer_pdf_queries",
    "writer":    "Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, mcp__alphaxiv__get_paper_content",
}
LEAD_TOOLS = ("Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, Task, "
              "mcp__alphaxiv__discover_papers, mcp__alphaxiv__get_paper_content, "
              "mcp__alphaxiv__answer_pdf_queries, mcp__alphaxiv__read_files_from_github_repository")

# Subagent display names referenced from commands / lead agent.
SUBAGENT_RENAME = {
    "researcher": "feynman-researcher",
    "verifier": "feynman-verifier",
    "reviewer": "feynman-reviewer",
    "writer": "feynman-writer",
}

# ---------------------------------------------------------------------------
# Layer 1: BLOCK_REWRITES — hand-audited prose replacements (applied FIRST, case-sensitive).
# These target the exact upstream sentences/blocks that forbid Claude Code tools or assume the Pi
# `subagent` tool / `alpha` CLI. A global token swap would corrupt these into self-contradictions
# ("use WebSearch; do not call WebSearch"), so they are rewritten wholesale.
# ---------------------------------------------------------------------------

_ALPHA_MCP_NOTE = ("Use the alphaXiv MCP tools (`mcp__alphaxiv__discover_papers`, "
                   "`mcp__alphaxiv__get_paper_content`, `mcp__alphaxiv__answer_pdf_queries`, "
                   "`mcp__alphaxiv__read_files_from_github_repository`) for academic paper search, "
                   "reading, Q&A, and repository inspection. If the alphaXiv MCP is unavailable, the "
                   "`alpha` CLI via `Bash` (`alpha search|get|ask|code`, after `alpha login`) is a fallback.")

BLOCK_REWRITES = [
    # --- prompts/*.md "Tool Discipline (Read First)" bullets -------------------------------------
    (r"Search with `web_search`; do not call `search_web`, `google_search`, `google:search`, "
     r"`search_google`, or `WebSearch`\.",
     "Search the web with the `WebSearch` tool."),
    (r"Fetch URLs with `fetch_content`; do not call bare `fetch`, `WebFetch`, `read_url_content`, "
     r"or pass an array as `url`\. Use `urls` for multiple URLs when the tool supports it\.",
     "Read URLs with the `WebFetch` tool."),
    (r"Use visible Feynman alpha tools such as `alpha_search` when present\. For shell access, "
     r"call `feynman alpha \.\.\.`; do not call the user's bare global `alpha` binary\.",
     _ALPHA_MCP_NOTE),
    (r"Do not use `Task` as an agent dispatcher\. Use only the visible `subagent` tool when it exists\.",
     "Delegate to subagents with the `Task` tool, setting `subagent_type` to "
     "`feynman-researcher`, `feynman-verifier`, or `feynman-reviewer`."),
    (r"To ask the user a question, write plain chat text and wait for the next user message\. "
     r"Do not call `ask_user_question`, `ask_user`, `ask_followup_question`, or `user_choice`\.",
     "To ask the user a question, write plain chat text and wait for the next user message."),

    # --- .feynman/SYSTEM.md sentences -------------------------------------------------------------
    (r"Use visible Feynman alpha tools such as `alpha_search`, `alpha_get_paper`, `alpha_ask_paper`, "
     r"and `alpha_read_code` for academic paper search, paper reading, paper Q&A, repository "
     r"inspection, and persistent annotations\.",
     _ALPHA_MCP_NOTE),
    (r"Use `web_search`, `fetch_content`, and `get_search_content` first for current topics:",
     "Use `WebSearch` and `WebFetch` first for current topics:"),
    (r"Tool names are literal\. For web search, call `web_search`; do not call non-existent aliases "
     r"such as `search_web`, `google:search`, `google_search`, or `search_google`\. For URL reading, "
     r"call `fetch_content`; do not call bare `fetch`, `WebFetch`, or `read_url_content`\.",
     "Tool names are literal: use `WebSearch` for web search and `WebFetch` for reading URLs."),
    (r"To ask the user a question, write plain chat text and wait for the next user message\. Do not "
     r"call non-existent question tools such as `ask_user_question`, `ask_user`, "
     r"`ask_followup_question`, or `user_choice`\.",
     "To ask the user a question, write plain chat text and wait for the next user message."),
    (r"For shell-based alphaXiv access, call `feynman alpha \.\.\.` through `bash`\. Do not call the "
     r"user's bare global `alpha` binary; it may be stale or unpatched\.",
     "If the alphaXiv MCP is unavailable, the `alpha` CLI via `Bash` (after `alpha login`) is a fallback."),

    # --- subagent dispatch (SYSTEM.md + prompts) --------------------------------------------------
    (r"Feynman ships project subagents for research work\. Prefer the `researcher`, `writer`, "
     r"`verifier`, and `reviewer` subagents",
     "Feynman ships project subagents for research work. Prefer the `feynman-researcher`, "
     "`feynman-writer`, `feynman-verifier`, and `feynman-reviewer` subagents (via the `Task` tool)"),
    (r"For detached long-running work, prefer background subagent execution with "
     r"`clarify: false, async: true`\.",
     "For independent subtasks, dispatch multiple `Task` calls in one turn to run them in parallel."),
    # Fenced JSON dispatch examples -> Task-tool prose (deepresearch and similar).
    (r"```json\n\{\s*\n\s*\"tasks\":.*?```",
     "Dispatch each researcher with the `Task` tool (`subagent_type: \"feynman-researcher\"`), one "
     "`Task` call per brief, multiple calls in a single turn to run them in parallel. Tell each its "
     "input brief path and its output file."),
    (r"```json\n\{\s*\n\s*\"agent\":\s*\"verifier\".*?```",
     "Run the verifier with the `Task` tool (`subagent_type: \"feynman-verifier\"`): add inline "
     "citations to the draft, verify every URL/paper claim, and write the cited brief."),
    (r"```json\n\{\s*\n\s*\"agent\":\s*\"reviewer\".*?```",
     "Run the reviewer with the `Task` tool (`subagent_type: \"feynman-reviewer\"`): flag unsupported "
     "claims, logical gaps, single-source critical claims, and overstated confidence."),
]

# ---------------------------------------------------------------------------
# Layer 2: TOOL_MAP — token-level substitutions (applied AFTER block rewrites).
# Backtick-wrapped tool names map 1:1 to Claude Code / alphaXiv MCP names.
# ---------------------------------------------------------------------------

TOOL_MAP = {
    "alpha_search": "mcp__alphaxiv__discover_papers",
    "alpha_get_paper": "mcp__alphaxiv__get_paper_content",
    "alpha_ask_paper": "mcp__alphaxiv__answer_pdf_queries",
    "alpha_read_code": "mcp__alphaxiv__read_files_from_github_repository",
    "web_search": "WebSearch",
    "fetch_content": "WebFetch",
    "get_search_content": "WebFetch",
}

# Pi tools that have no Claude equivalent: rewrite their backticked mentions to a plain phrase so no
# dangling `memory_remember`-style tokens remain. (Sentence-level prose around them is largely in
# SYSTEM.md; these keep individual references grammatical.)
DROP_MAP = {
    "memory_remember": "a note written to disk",
    "memory_search": "notes read from disk",
    "memory_lessons": "lessons saved to disk",
    "schedule_prompt": "an external cron job",
    "subagent_status": "the Task result",
    "hf_dataset_info": "WebFetch on the dataset card",
    "hf_repo_files": "WebFetch on the repo",
    "hf_repo_read_file": "WebFetch on the file",
    "init_experiment": "Bash",
    "run_experiment": "Bash",
    "log_experiment": "Bash",
    "pi-charts": "Mermaid diagrams",
}


# Plain-text phrase rewrites for alpha-CLI framing that the block/token layers don't cover:
# make the alphaXiv MCP primary and the bare `alpha` CLI (alpha-hub) the documented fallback.
PHRASE_REWRITES = [
    ("Feynman's alphaXiv-backed alpha tools", "the alphaXiv MCP tools"),
    ("visible Feynman alpha tools", "the alphaXiv MCP tools"),
    ("Feynman's alpha tools", "the alphaXiv MCP tools"),
    ("alpha-backed paper search", "alphaXiv MCP paper search"),
    ("alpha-backed tools", "the alphaXiv MCP"),
    ("; do not call the user's bare global `alpha` binary because it can be stale or unpatched.",
     " as a fallback."),
    (", not a bare global `alpha search`.", "."),
    (", not a bare global `alpha` binary.", "."),
    ("feynman alpha ", "alpha "),  # wrapper -> bare alpha-hub CLI (the documented fallback)
]


def apply_phrase_rewrites(text: str) -> str:
    for old, new in PHRASE_REWRITES:
        text = text.replace(old, new)
    return text


def clean_desc(desc: str) -> str:
    return apply_phrase_rewrites(desc)


def _backtick(token: str) -> re.Pattern:
    return re.compile(r"`" + re.escape(token) + r"`")


def apply_block_rewrites(text: str) -> str:
    for pattern, replacement in BLOCK_REWRITES:
        text = re.sub(pattern, replacement, text, flags=re.DOTALL)
    return text


def apply_tool_map(text: str) -> str:
    for token, repl in TOOL_MAP.items():
        text = _backtick(token).sub("`" + repl + "`", text)
    for token, repl in DROP_MAP.items():
        text = _backtick(token).sub(repl, text)
    return text


def substitute(text: str) -> str:
    """Full conversion: hand-audited block rewrites, token map, then phrase rewrites."""
    text = apply_block_rewrites(text)
    text = apply_tool_map(text)
    text = apply_phrase_rewrites(text)
    # `subagent` (Pi dispatch tool) -> `Task` (bare tool name, so "the `subagent` tool" -> "the
    # `Task` tool" rather than doubling "the"/"tool"). Block rewrites handle the longer phrases.
    text = re.sub(r"`subagent`", "`Task`", text)
    # $@ argument placeholder -> Claude Code $ARGUMENTS
    text = text.replace("$@", "$ARGUMENTS")
    # Backticked subagent name references -> feynman-prefixed.
    for old, new in SUBAGENT_RENAME.items():
        text = _backtick(old).sub("`" + new + "`", text)
    # JSON "agent": "researcher" -> "subagent_type": "feynman-researcher" (any survivors).
    for old, new in SUBAGENT_RENAME.items():
        text = re.sub(r'"agent":\s*"' + old + r'"', '"subagent_type": "' + new + '"', text)
    return text


def parse_frontmatter(text: str):
    """Parse YAML-ish frontmatter. Returns (metadata dict, body)."""
    m = re.match(r"^---\n(.*?)\n---\n?(.*)", text, re.DOTALL)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).split("\n"):
        sep = line.find(":")
        if sep == -1:
            continue
        key = line[:sep].strip()
        val = line[sep + 1:].strip()
        if key:
            fm[key] = val
    return fm, m.group(2)


def process_command(prompt_path: Path):
    """prompts/<name>.md -> commands/feynman/<name>.md (Claude slash command)."""
    name = prompt_path.stem
    fm, body = parse_frontmatter(prompt_path.read_text())
    desc = clean_desc(fm.get("description", f"Feynman {name} workflow."))
    arg_hint = fm.get("args", "<topic>")
    body = substitute(body).strip()
    out = f"---\ndescription: {desc}\nargument-hint: {arg_hint}\n---\n\n{body}\n"
    COMMANDS_OUT.mkdir(parents=True, exist_ok=True)
    (COMMANDS_OUT / f"{name}.md").write_text(out)
    return name


def process_skill(skill_md: Path):
    """skills/<name>/SKILL.md -> skills/<name>/SKILL.md (preserve frontmatter, substitute body)."""
    name = skill_md.parent.name
    fm, body = parse_frontmatter(skill_md.read_text())
    desc = clean_desc(fm.get("description", f"Feynman {name} skill."))
    body = substitute(body).strip()
    out_dir = SKILLS_OUT / name
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "SKILL.md").write_text(f"---\nname: {name}\ndescription: {desc}\n---\n\n{body}\n")
    return name


def process_agent(agent_path: Path):
    """.feynman/agents/<name>.md -> agents/feynman-<name>.md (Claude subagent)."""
    name = agent_path.stem
    fm, body = parse_frontmatter(agent_path.read_text())
    desc = clean_desc(fm.get("description", f"Feynman {name} subagent."))
    tools = AGENT_TOOLS.get(name)
    body = substitute(body).strip()
    out_name = f"feynman-{name}"
    fm_lines = [f"name: {out_name}", f"description: {desc}"]
    if tools:
        fm_lines.append(f"tools: {tools}")
    fm_lines.append("model: inherit")
    AGENTS_OUT.mkdir(parents=True, exist_ok=True)
    (AGENTS_OUT / f"{out_name}.md").write_text("---\n" + "\n".join(fm_lines) + f"\n---\n\n{body}\n")
    return out_name


def process_lead_agent():
    """.feynman/SYSTEM.md -> agents/feynman.md (lead research agent)."""
    system_path = FEYNMAN_DIR / ".feynman" / "SYSTEM.md"
    if not system_path.exists():
        print("  ! SYSTEM.md not found")
        return
    body = substitute(system_path.read_text()).strip()
    desc = ("Research-first AI agent. Use for deep investigation, evidence synthesis, literature "
            "reviews, paper audits, or any research-heavy task.")
    fm = f"---\nname: feynman\ndescription: {desc}\ntools: {LEAD_TOOLS}\nmodel: inherit\n---\n\n"
    (AGENTS_OUT / "feynman.md").write_text(fm + body + "\n")


def main():
    print(f"Generating Claude Code assets from: {FEYNMAN_DIR}")
    print(f"  Output: {OUTPUT_DIR}\n")
    if not FEYNMAN_DIR.exists():
        print(f"ERROR: feynman submodule not found at {FEYNMAN_DIR}")
        print("  Run: git submodule update --init")
        sys.exit(1)

    for d in (COMMANDS_OUT, SKILLS_OUT, AGENTS_OUT):
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)

    print("Commands (from prompts/):")
    for p in sorted((FEYNMAN_DIR / "prompts").glob("*.md")):
        print(f"  /feynman:{process_command(p)}")

    print("\nSkills (from skills/):")
    for skill_md in sorted((FEYNMAN_DIR / "skills").glob("*/SKILL.md")):
        print(f"  {process_skill(skill_md)}")

    print("\nAgents (from .feynman/agents/):")
    for a in sorted((FEYNMAN_DIR / ".feynman" / "agents").glob("*.md")):
        print(f"  {process_agent(a)}")
    print("  feynman (lead)")
    process_lead_agent()

    n_cmd = len(list(COMMANDS_OUT.glob("*.md")))
    n_skill = sum(1 for _ in SKILLS_OUT.iterdir() if _.is_dir())
    n_agent = len(list(AGENTS_OUT.glob("*.md")))
    print(f"\nGenerated {n_cmd} commands, {n_skill} skills, {n_agent} agents.")


if __name__ == "__main__":
    main()
