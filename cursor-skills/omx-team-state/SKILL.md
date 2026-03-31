---
name: omx-team-state
description: >-
  File-based state schema and lifecycle manager for team orchestration under
  .cursor/state/team/.
---
# Team State (Phase 4)

## Purpose
Define and maintain a deterministic state contract for team orchestration so parallel runs are traceable, resumable, and auditable.

## When to Use
- Starting any `omx-team-orchestrator` run
- Resuming an interrupted team run
- Diagnosing failed or partial orchestration
- Generating post-run audit/completion reports

## State Root
`.cursor/state/team/<teamId>/`

## Required Files

### `config.json`
Team metadata and immutable configuration.

Suggested shape:
```json
{
  "teamId": "team-2026-03-31-auth-refactor",
  "createdAt": "2026-03-31T18:20:00Z",
  "objective": "Ship feature with parallel execution",
  "constraints": ["no schema changes"],
  "workerCount": 3,
  "executionMode": "hybrid",
  "status": "active"
}
```

### `progress.json`
Live counters and current phase.

```json
{
  "phase": "dispatch",
  "pending": 4,
  "in_progress": 2,
  "completed": 1,
  "failed": 0,
  "lastUpdatedAt": "2026-03-31T18:24:00Z"
}
```

### `tasks/task-<id>.json`
Atomic task records.

```json
{
  "taskId": "task-003",
  "title": "Implement parser fix",
  "lane": "execution",
  "dependencies": ["task-001"],
  "assignee": "worker-2",
  "status": "in_progress",
  "paths": ["src/parser.py"]
}
```

### `results/result-<id>.json`
Worker output payload.

```json
{
  "taskId": "task-003",
  "worker": "worker-2",
  "status": "completed",
  "changedFiles": ["src/parser.py"],
  "verification": [
    {"command": "pytest tests/parser -q", "status": "pass"}
  ]
}
```

### `audit-log.json`
Chronological event stream.

```json
[
  {"ts":"2026-03-31T18:20:00Z","event":"team_created"},
  {"ts":"2026-03-31T18:22:00Z","event":"tasks_dispatched","count":3}
]
```

## Optional Files
- `merge-report.json`
- `completion-report.json`
- `errors.json`

## Lifecycle
1. **Init**: create directory + `config.json`, `progress.json`, empty `audit-log.json`.
2. **Dispatch**: create/transition task files; append dispatch events.
3. **Execution**: write results and update counters.
4. **Verification**: append review/check results.
5. **Complete**: write `completion-report.json`, mark status complete.

## Auto Mode Guidelines
- Always write state updates before dispatching next phase.
- Avoid in-memory-only coordination when state file exists.
- If state is inconsistent, pause orchestration and reconcile from task/result files.
- Keep every event append-only in `audit-log.json`.

## Validation Rules
- Every `task-*.json` must have a unique `taskId`.
- `progress.json` counts must reconcile with task statuses.
- `results/*.json` must reference existing `taskId`.
- `completion-report.json` requires final verification summary.
