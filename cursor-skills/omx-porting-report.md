# OmX-to-Cursor Porting Report

**Date**: March 31, 2026  
**Source**: [Yeachan-Heo/oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex) v0.11.10 (MIT License)  
**Target**: Global Cursor config (`C:\Users\khala\.cursor\`)

---

## Summary

| Category | Total | Converted | Skipped | Avg Score |
|----------|-------|-----------|---------|-----------|
| Prompts (-> Cursor Rules) | 33 | 33 | 0 | 95.5/100 |
| Skills (-> Cursor Skills) | 36 | 21 | 15 | 100.0/100 |
| **Total** | **69** | **54** | **15** | **97.3/100** |

**Validation iterations required**: 1 (all files passed on first attempt)

---

## Phase 1: Prompts -> Cursor Rules (33 files)

All 33 OmX agent prompts were converted to `.mdc` rule files in `C:\Users\khala\.cursor\rules\`.

| # | Rule File | Score | Original OmX Prompt |
|---|-----------|-------|---------------------|
| 1 | `omx-analyst.mdc` | 95 | analyst |
| 2 | `omx-api-reviewer.mdc` | 95 | api-reviewer |
| 3 | `omx-architect.mdc` | 95 | architect |
| 4 | `omx-build-fixer.mdc` | 95 | build-fixer |
| 5 | `omx-code-reviewer.mdc` | 95 | code-reviewer |
| 6 | `omx-code-simplifier.mdc` | 100 | code-simplifier |
| 7 | `omx-critic.mdc` | 95 | critic |
| 8 | `omx-debugger.mdc` | 95 | debugger |
| 9 | `omx-dependency-expert.mdc` | 95 | dependency-expert |
| 10 | `omx-designer.mdc` | 95 | designer |
| 11 | `omx-executor.mdc` | 95 | executor |
| 12 | `omx-explore-harness.mdc` | 100 | explore-harness |
| 13 | `omx-explore.mdc` | 95 | explore |
| 14 | `omx-git-master.mdc` | 95 | git-master |
| 15 | `omx-information-architect.mdc` | 95 | information-architect |
| 16 | `omx-performance-reviewer.mdc` | 95 | performance-reviewer |
| 17 | `omx-planner.mdc` | 95 | planner |
| 18 | `omx-product-analyst.mdc` | 95 | product-analyst |
| 19 | `omx-product-manager.mdc` | 95 | product-manager |
| 20 | `omx-qa-tester.mdc` | 95 | qa-tester |
| 21 | `omx-quality-reviewer.mdc` | 95 | quality-reviewer |
| 22 | `omx-quality-strategist.mdc` | 95 | quality-strategist |
| 23 | `omx-researcher.mdc` | 95 | researcher |
| 24 | `omx-security-reviewer.mdc` | 95 | security-reviewer |
| 25 | `omx-sisyphus-lite.mdc` | 95 | sisyphus-lite |
| 26 | `omx-style-reviewer.mdc` | 95 | style-reviewer |
| 27 | `omx-team-executor.mdc` | 100 | team-executor |
| 28 | `omx-team-orchestrator.mdc` | 95 | team-orchestrator |
| 29 | `omx-test-engineer.mdc` | 95 | test-engineer |
| 30 | `omx-ux-researcher.mdc` | 95 | ux-researcher |
| 31 | `omx-verifier.mdc` | 95 | verifier |
| 32 | `omx-vision.mdc` | 95 | vision |
| 33 | `omx-writer.mdc` | 95 | writer |

---

## Phase 2: Skills -> Cursor Skills (21 files)

All 21 applicable OmX skills were converted to SKILL.md files in `C:\Users\khala\.cursor\skills-cursor\omx-{name}\`.

| # | Skill Directory | Score | Original OmX Skill |
|---|-----------------|-------|---------------------|
| 1 | `omx-ai-slop-cleaner/` | 100 | ai-slop-cleaner |
| 2 | `omx-analyze/` | 100 | analyze |
| 3 | `omx-autopilot/` | 100 | autopilot |
| 4 | `omx-build-fix/` | 100 | build-fix |
| 5 | `omx-code-review/` | 100 | code-review |
| 6 | `omx-deep-interview/` | 100 | deep-interview |
| 7 | `omx-deepsearch/` | 100 | deepsearch |
| 8 | `omx-frontend-ui-ux/` | 100 | frontend-ui-ux |
| 9 | `omx-git-master/` | 100 | git-master |
| 10 | `omx-pipeline/` | 100 | pipeline |
| 11 | `omx-plan/` | 100 | plan |
| 12 | `omx-ralph/` | 100 | ralph |
| 13 | `omx-ralph-init/` | 100 | ralph-init |
| 14 | `omx-ralplan/` | 100 | ralplan |
| 15 | `omx-review/` | 100 | review |
| 16 | `omx-security-review/` | 100 | security-review |
| 17 | `omx-tdd/` | 100 | tdd |
| 18 | `omx-ultraqa/` | 100 | ultraqa |
| 19 | `omx-ultrawork/` | 100 | ultrawork |
| 20 | `omx-visual-verdict/` | 100 | visual-verdict |
| 21 | `omx-web-clone/` | 100 | web-clone |

---

## Skipped Skills (15) -- with Reasons

These OmX skills were not converted because they are tied to OmX-specific infrastructure (tmux, MCP servers, CLI commands) that has no meaningful Cursor equivalent.

| # | Skill | Reason for Skipping |
|---|-------|---------------------|
| 1 | `ask-claude` | External model delegation -- Cursor already uses Claude as its underlying model |
| 2 | `ask-gemini` | External model delegation -- requires Gemini API key and custom MCP server |
| 3 | `cancel` | OmX process cancellation -- Cursor handles task cancellation natively |
| 4 | `configure-notifications` | OmX notification gateway (Slack, Discord, email) -- no Cursor equivalent |
| 5 | `doctor` | OmX installation diagnostics (`omx doctor`) -- not applicable to Cursor |
| 6 | `ecomode` | OmX token-saving mode -- Cursor handles model/token management internally |
| 7 | `help` | OmX help command (`omx help`) -- Cursor has its own help system |
| 8 | `hud` | OmX heads-up display monitoring (`omx hud --watch`) -- requires tmux |
| 9 | `note` | OmX session note-taking (`.omx/notes/`) -- can use Cursor rules or workspace files |
| 10 | `omx-setup` | OmX installation/scaffolding (`omx setup`) -- not applicable to Cursor |
| 11 | `skill` | OmX skill management CLI -- Cursor uses SKILL.md files directly |
| 12 | `swarm` | Multi-agent swarm orchestration -- requires tmux/psmux for durable sessions |
| 13 | `team` | Coordinated parallel team execution -- requires tmux/worktree infrastructure beyond Cursor's Task tool |
| 14 | `trace` | OmX execution tracing/debugging -- relies on OmX-specific MCP state server |
| 15 | `worker` | OmX worker subprocess management -- requires tmux session lifecycle |

---

## Tool Mapping Reference

All OmX/Codex tool references were mapped to Cursor equivalents during conversion:

| OmX/Codex Tool | Cursor Equivalent |
|----------------|-------------------|
| `ask_codex` (with agent_role) | `Task tool` (subagent with appropriate subagent_type) |
| `AskUserQuestion` | `AskQuestion tool` |
| `lsp_diagnostics` | `ReadLints tool` |
| `ast_grep_search` | `Grep tool` |
| `Bash` / `shell` | `Shell tool` |
| `Edit` / `file_edit` | `StrReplace tool` |
| `Read` | `Read tool` (unchanged) |
| `Write` | `Write tool` (unchanged) |
| `Glob` | `Glob tool` (unchanged) |
| `Grep` | `Grep tool` (unchanged) |
| `.omx/` directory paths | `.cursor/` directory paths |
| `omx explore` | `Task tool with explore subagent` |
| `omx team` | `Task tool with parallel subagents` |
| `omx sparkshell` | `Shell tool` |
| `$ralph` skill reference | `omx-ralph skill` |
| `$plan` skill reference | `omx-plan skill` |
| `$team` skill reference | `Task tool with parallel subagents` |
| `$autopilot` skill reference | `omx-autopilot skill` |
| `$deep-interview` skill reference | `omx-deep-interview skill` |
| `$visual-verdict` skill reference | `omx-visual-verdict skill` |
| `ToolSearch("mcp")` | Removed (not applicable in Cursor) |
| `state_write` / `state_read` MCP | Removed (Cursor is stateless per session) |
| `delegate(role="...")` | `Task tool (subagent)` |

---

## Known Limitations

1. **No persistent state across sessions**: OmX uses `.omx/state/` and MCP state servers for cross-session memory. Cursor skills are stateless per conversation. Skills referencing state persistence have been adapted to use workspace files instead.

2. **No tmux/worktree orchestration**: OmX's `$team` mode creates isolated git worktrees per worker via tmux. Cursor's Task tool supports parallel subagents but they share the workspace. The `best-of-n-runner` subagent type provides some worktree isolation but is not a full replacement.

3. **No HUD monitoring**: OmX provides a real-time terminal HUD (`omx hud --watch`). Cursor has no equivalent real-time monitoring surface.

4. **Model routing differences**: OmX supports mixed-provider workers (Codex, Claude, Gemini). Cursor rules/skills run on whatever model Cursor is configured with.

5. **Skill invocation**: In OmX, skills are invoked with `$skillname "task"`. In Cursor, skills are invoked by the agent automatically based on the `description` field in SKILL.md, or by the user referencing them explicitly.

6. **MCP tool discovery**: OmX uses `ToolSearch("mcp")` for runtime tool discovery. Cursor discovers MCP tools through its configuration. References to ToolSearch have been removed.

---

## Validation Script

The validation script used for accuracy verification is located at:  
`scripts/omx-validation/validate.py`

Usage:
```
python validate.py prompts    # Validate prompt conversions
python validate.py skills     # Validate skill conversions
python validate.py prompts --json   # JSON output
```
