---
name: omx-pipeline
description: >-
  Configurable pipeline orchestrator for sequencing stages through planning,
  execution, and verification with state persistence and resume support.
  Ported from OmX $pipeline for Cursor agent use.
---
# Pipeline (ported from OmX $pipeline)

## Purpose

The pipeline skill is a configurable orchestrator for sequencing stages through a uniform interface, with state persistence and resume support. It sequences consensus planning, parallel execution, and architect verification into a coherent workflow.

## When to Use

- Task requires a structured multi-stage workflow (plan -> execute -> verify)
- Work benefits from staged coordination with state persistence
- Task is large enough to warrant the overhead of a full pipeline
- User wants autonomous execution with built-in verification gates

## When Not to Use

- Simple single-step tasks — just do them directly
- User wants manual control over each phase — use individual skills instead
- Quick fixes or one-shot changes — delegate to an executor directly

## Default Pipeline

The canonical pipeline sequences:

```
RALPLAN (consensus planning) -> team-exec (parallel subagents) -> ralph-verify (architect verification)
```

## Configuration

Pipeline parameters are configurable per run:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `maxRalphIterations` | 10 | Ralph verification iteration ceiling |
| `workerCount` | 2 | Number of parallel subagent workers |
| `agentType` | `executor` | Agent type for team workers |

## Workflow

### Built-in Stages

1. **ralplan** — Consensus planning (planner + architect + critic via Task tool subagents). Skips only when both PRD and test-spec planning artifacts already exist, and carries any deep-interview spec paths forward for traceability.
2. **team-exec** — Team execution via Task tool with parallel subagents. Always the execution backend.
3. **ralph-verify** — Ralph verification loop with configurable iteration count.

### State Management

Pipeline state persists via the project workspace:

- **On start**: Record pipeline mode as active, current phase as `stage:ralplan`
- **On stage transitions**: Update current phase to `stage:<name>`
- **On completion**: Mark pipeline as inactive, phase as `complete`

Resume is supported from the last incomplete stage.

## Tools

- **Task tool (subagent)** with `subagent_type: "generalPurpose"` — delegate planning, execution, and verification to specialist subagents
- **Task tool (subagent)** with `subagent_type: "explore"` — codebase exploration during planning
- **Shell tool** — run builds, tests, and verification commands
- **ReadLints tool** — check for linter errors after execution
- **StrReplace tool** — apply code changes during execution stages

## Relationship to Other Skills

- **omx-autopilot**: Autopilot can use pipeline as its execution engine
- **omx-ralph**: Pipeline delegates verification to ralph (configurable iterations)
- **omx-ralplan**: Pipeline's first stage runs RALPLAN consensus planning
- **Task tool with parallel subagents**: Pipeline delegates execution to parallel subagents
