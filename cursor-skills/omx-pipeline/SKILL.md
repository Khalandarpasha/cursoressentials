---
name: omx-pipeline
description: >-
  Configurable pipeline orchestrator for planning, team execution, and
  verification with explicit artifact contracts, recovery gates, and progress
  reporting.
---
# Pipeline (ported from OmX $pipeline)

## Purpose
Run a deterministic multi-stage delivery flow:
`planning -> team execution -> verification`, with explicit handoff artifacts and recovery behavior.

## OmX Parity Notes
This skill preserves the original pipeline intent:
- canonical stage shape: `RALPLAN -> team-exec -> ralph-verify`
- stateful phase tracking and resume from last incomplete stage
- team execution as the main parallel backend

OmX used `.omx/state/pipeline-state.json`, Codex CLI team workers, and tmux runtime.
Cursor adaptation uses `.cursor/state`, `omx-team-orchestrator`, and Task-based workers.

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
Canonical stage order:
1. `ralplan` (consensus planning)
2. `team-exec` (omx-team-orchestrator execution stage)
3. `ralph-verify` (verification and closure)

## Configuration
Pipeline parameters are configurable per run:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `maxRalphIterations` | 10 | Ralph verification iteration ceiling |
| `workerCount` | 2 | Number of execution workers |
| `agentType` | `executor` | Execution role hint |
| `stageTimeoutMinutes` | 45 | Soft timeout per stage |
| `maxRetriesPerStage` | 2 | Recovery retry limit |
| `progressUpdateSeconds` | 30 | Progress report cadence |

## Workflow

### Stage Contracts (Required Artifacts)

#### Stage 1: `ralplan`
Required outputs:
- `.cursor/plans/plan-<slug>.md`
- `.cursor/plans/acceptance-criteria-<slug>.md`
- `.cursor/plans/task-breakdown-<slug>.json`

#### Stage 2: `team-exec`
Required inputs:
- `task-breakdown-<slug>.json`
- acceptance criteria file

Required outputs:
- `.cursor/state/team/<teamId>/completion-report.json`
- `.cursor/state/team/<teamId>/merge-report.json` (if conflicts occurred)

Execution backend:
- Delegate to `omx-team-orchestrator`.

#### Stage 3: `ralph-verify`
Required inputs:
- stage-2 completion report
- verification command set

Required outputs:
- final verification summary
- residual risk list

### Recovery and Error Handling
If a stage fails:
1. Write stage error snapshot under `.cursor/state/pipeline/errors-<stage>.json`.
2. Retry up to `maxRetriesPerStage`.
3. If still failing, escalate with:
   - failure root cause
   - blocking dependency
   - recommended remediation path

### Timeout Guidance
- Soft timeout per stage: `stageTimeoutMinutes`
- On timeout:
  1. checkpoint current state
  2. mark stage as `timed_out`
  3. ask user whether to continue, reduce scope, or abort

### Progress Reporting
- Emit progress update every `progressUpdateSeconds`:
  - current stage
  - completed vs pending tasks
  - current blockers
  - ETA confidence (high/medium/low)

### State Management

Pipeline state persists via the project workspace:

- **On start**: Record pipeline mode as active, current phase as `stage:ralplan`
- **On stage transitions**: Update current phase to `stage:<name>`
- **On completion**: Mark pipeline as inactive, phase as `complete`

Resume is supported from the last incomplete stage.

## Tools

- **Task tool (subagent)** with `subagent_type: "generalPurpose"` for planning/review lanes
- **Task tool (subagent)** with `subagent_type: "explore"` for discovery
- **Task tool (subagent)** with `subagent_type: "best-of-n-runner"` for isolated execution workers
- **Shell tool** for tests/build/verification
- **ReadLints tool** for static diagnostics
- **StrReplace tool** for targeted local edits

## Relationship to Other Skills

- **omx-autopilot**: can call this pipeline as the execution backbone
- **omx-ralplan**: default planning stage
- **omx-team-orchestrator**: default execution stage
- **omx-ralph**: default verification stage
- **omx-conflict-resolver**: invoked when stage-2 merge collisions occur

## Completion Criteria
- All stage contracts satisfied
- No unresolved blocking error in pipeline state
- Verification stage passed
- Final report includes limitations/residual risk
