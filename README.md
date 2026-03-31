# Cursor Essentials: OmX-to-Cursor Port

This repository packages the assets generated from an OmX (`oh-my-codex`) to Cursor migration.

It includes:
- 33 converted Cursor Rules (`.mdc`)
- 21 converted Cursor Skills (`SKILL.md`)
- 4 Phase-4 orchestration artifacts (`omx-team-orchestrator`, `omx-team-worker`, `omx-team-state`, `omx-conflict-resolver`)
- Validation script used to score conversion quality against original OmX files
- Full migration report with scores, skipped items, and mapping decisions

## Repository Layout

- `cursor-rules/`  
  Converted rules from OmX prompts. File pattern: `omx-*.mdc`
- `cursor-skills/`  
  Converted skills. Each skill is in `omx-<name>/SKILL.md`
- `scripts/omx-validation/validate.py`  
  Validator that checks converted files against OmX source with a 100-point rubric
- `scripts/omx-validation/validate-phase4.py`  
  Phase-4 validator for team orchestration parity vs OmX team/worker/pipeline/ultrawork/swarm
- `omx-porting-report.md`  
  Final scorecard and migration details

## What To Use, When, and Why

### 1) Use Rules (`cursor-rules/*.mdc`) for role behavior
Use rules when you want Cursor to adopt a repeatable behavior profile while working.

Best for:
- Architecture analysis (`omx-architect.mdc`)
- Code review posture (`omx-code-reviewer.mdc`)
- Debug strategy (`omx-debugger.mdc`)
- Security/performance review lenses (`omx-security-reviewer.mdc`, `omx-performance-reviewer.mdc`)

When to use:
- You need consistent response style and review depth
- You want reusable constraints/checklists across projects
- You want role-based guidance but not full workflow orchestration

When not to use:
- You need multi-step orchestration logic (use skills)
- You need execution loops or parallel agents (use skills)

### 2) Use Skills (`cursor-skills/omx-*/SKILL.md`) for workflows
Use skills when the task is process-heavy and requires step sequencing, handoffs, or gating.

Best for:
- Planning flows (`omx-plan`, `omx-ralplan`)
- Persistent execution strategy (`omx-ralph`, `omx-autopilot`)
- Quality and testing workflows (`omx-review`, `omx-security-review`, `omx-tdd`, `omx-ultraqa`)
- Specialized task pipelines (`omx-ultrawork`, `omx-build-fix`)

When to use:
- The task has multiple phases (discover -> plan -> execute -> verify)
- You want explicit completion criteria and repeatable process
- You want Cursor to choose structured next steps instead of ad-hoc responses

When not to use:
- Single quick edits
- One-off Q&A

### 3) Use Validator (`scripts/omx-validation/validate.py`) for accuracy checks
Use the validator whenever you change any rule/skill and need objective quality confirmation.

Scoring target:
- Minimum acceptable accuracy: **90+ per file**

Checks include:
- Frontmatter quality
- Role/rules/workflow/output preservation
- Tool mapping correctness
- Completeness and section parity

For team orchestration parity (Phase 4), use:
- `scripts/omx-validation/validate-phase4.py`

## Quick Start

### A) Validate current assets
From this repo root:

```powershell
python .\scripts\omx-validation\validate.py prompts --source "c:\azuria_repo\_omx_source" --target-rules ".\cursor-rules"
python .\scripts\omx-validation\validate.py skills --source "c:\azuria_repo\_omx_source" --target-skills ".\cursor-skills"
```

Optional JSON output:

```powershell
python .\scripts\omx-validation\validate.py prompts --source "c:\azuria_repo\_omx_source" --target-rules ".\cursor-rules" --json
```

Phase 4 validation:

```powershell
python .\scripts\omx-validation\validate-phase4.py
```

### B) Install to global Cursor profile
If you want these globally available:

```powershell
Copy-Item .\cursor-rules\omx-*.mdc "C:\Users\khala\.cursor\rules\" -Force
Copy-Item .\cursor-skills\omx-* "C:\Users\khala\.cursor\skills-cursor\" -Recurse -Force
```

### C) Project-local install (recommended for team repos)
For repository-specific behavior:

```powershell
New-Item -ItemType Directory -Force -Path .\.cursor\rules | Out-Null
New-Item -ItemType Directory -Force -Path .\.cursor\skills | Out-Null
Copy-Item .\cursor-rules\omx-*.mdc .\.cursor\rules\ -Force
Copy-Item .\cursor-skills\omx-* .\.cursor\skills\ -Recurse -Force
```

## Recommended Usage Patterns

### Pattern 1: Feature delivery with guardrails
1. Start with `omx-planner` or `omx-plan`
2. Execute with `omx-ralph` or `omx-autopilot`
3. Validate with `omx-review` + `omx-security-review`
4. Use `omx-ultraqa` for stricter verification

### Pattern 2: Risk-sensitive changes
1. Apply `omx-architect` and `omx-security-reviewer` rules
2. Use `omx-ralplan` for consensus planning
3. Execute with `omx-ultrawork`
4. Finish with `omx-tdd` and validator checks

### Pattern 3: Large refactor
1. Analyze with `omx-analyze` + `omx-information-architect`
2. Break down with `omx-pipeline`
3. Implement via `omx-ralph`
4. Review with `omx-code-review` and `omx-quality-reviewer`

### Pattern 4: Team-native parallel orchestration (Phase 4)
1. Use `omx-team-orchestrator` to decompose and staff lanes
2. Run execution lanes on `best-of-n-runner` workers
3. Persist lifecycle in `.cursor/state/team/` via `omx-team-state`
4. Resolve overlaps with `omx-conflict-resolver`
5. Finalize via verification lanes and completion report

## Known Limits (Important)

These assets intentionally exclude OmX-only infrastructure behavior:
- tmux/psmux durable team runtimes
- OmX HUD and notification gateway features
- OmX-specific MCP state/tracing internals

See `omx-porting-report.md` for the complete skip list and rationale.

## Provenance

- Source framework: `Yeachan-Heo/oh-my-codex`
- Converted into Cursor-compatible rule/skill structure
- Validated against source content with rubric-based scoring

## Acknowledgement

This project is inspired by and derived from patterns in `oh-my-codex (OmX)` by Yeachan Heo:

- Upstream repository: [Yeachan-Heo/oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex)
- Upstream license: MIT

No proprietary source code is included here. This repository contains adaptation artifacts (rules/skills/validation workflow) prepared for Cursor usage.

## License

This repository is released under the MIT License. See `LICENSE`.

## Maintainer Notes

If you modify rules or skills:
1. Re-run validator for the affected category
2. Keep per-file score >= 90
3. Update `omx-porting-report.md` if additions/removals happen
4. Prefer tool mapping consistency across all files
