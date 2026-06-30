---
name: watch
description: Create a research watch baseline and optionally schedule follow-up checks when scheduling tools are visible. Use when the user asks to monitor a field, track new papers, watch for updates, or set up alerts on a research area.
---

# Watch

Run the `/watch` workflow. The slash command expands the full workflow instructions in the active session; do not try to read a relative prompt-template path from the installed skill directory.

Agents used: `feynman-researcher`

Output: baseline survey in `outputs/`, plus a scheduled follow-up only when an external cron job is visible. If scheduling is unavailable, the workflow records that block instead of claiming a recurring watch exists.
