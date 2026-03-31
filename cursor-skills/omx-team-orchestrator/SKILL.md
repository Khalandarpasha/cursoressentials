---
name: omx-team-orchestrator
description: >-
  Cursor-native team orchestration skill that replicates OmX $team patterns
  using Task subagents, best-of-n-runner execution workers, and file-based
  state in .cursor/state/team/.
---
# Team Orchestrator (Phase 4)

## Purpose
Run durable multi-agent execution in Cursor with explicit staffing, dispatch, monitoring, merge, and verification gates.

## When to Use
- Task is broad and decomposable across 2+ lanes
- You need independent execution workers plus reviewer lanes
- You want a stateful audit trail in `.cursor/state/team/`
- You need best-of-n worktree isolation for execution safety

## When Not to Use
- Tiny one-file changes
- Work with strict sequential dependencies only
- User requested minimal/no orchestration overhead

## Core Runtime Model
- **Execution workers**: `Task` with `subagent_type: "best-of-n-runner"` (isolated worktree)
- **Reviewer lanes**: `Task` with `subagent_type: "generalPurpose"`
- **State backbone**: `.cursor/state/team/` JSON artifacts
- **Leader loop**: read state -> dispatch -> collect -> verify -> finalize

## OmX Parity Notes
This skill intentionally mirrors the OmX Team contract semantics:
- team-first launch posture with conservative staffing
- explicit dispatch and mailbox-like coordination via state files
- durable lifecycle control (init -> dispatch -> monitor -> cleanup)
- evidence-backed completion instead of optimistic completion

Original OmX references include tmux panes, `omx team api`, and `.omx/state/team/...`.
Cursor adaptation replaces those with Task subagents, best-of-n worktrees, and `.cursor/state/team/...`.

## Seven-Phase Workflow

### Phase 0: Context Intake and Snapshot
1. Normalize the user task into one objective statement.
2. Create `config.json` and `progress.json` under `.cursor/state/team/<teamId>/`.
3. Capture constraints, unknowns, acceptance criteria, and touched paths.
4. If ambiguity is high, delegate a quick explore pass before dispatch.

### Phase 1: Task Decomposition
1. Split work into atomic tasks with explicit dependencies.
2. Write task specs to `.cursor/state/team/<teamId>/tasks/task-*.json`.
3. Tag each task with lane type:
   - `execution` (best-of-n-runner)
   - `review` (generalPurpose)
   - `verification` (generalPurpose or shell)

### Phase 2: Staffing
1. Assign worker count and roles from decomposition.
2. Enforce conservative fanout:
   - default 2 execution workers
   - max 4 unless user explicitly requests more
3. Reserve reviewer lanes (architect + security) for high-risk changes.

### Phase 3: Parallel Dispatch
1. Launch independent execution tasks in one parallel Task message.
2. Use `best-of-n-runner` for code-writing tasks.
3. Run long shell checks in background with `block_until_ms: 0`.
4. Record dispatch events in `audit-log.json`.

### Phase 4: Collect and Monitor
1. Poll task completions and append worker output into `results/*.json`.
2. Update `progress.json` counters (`pending`, `in_progress`, `completed`, `failed`).
3. If a worker fails repeatedly, pause dependent tasks and escalate.

### Phase 5: Conflict Resolution and Merge
1. Detect overlapping file edits from worker results.
2. Prefer clean cherry-pick path when non-overlapping.
3. Use three-way merge for overlapping edits.
4. Delegate complex merges to `omx-conflict-resolver`.
5. Write merge decisions into `merge-report.json`.

### Phase 6: Verification Lanes
1. Launch architect reviewer lane (`generalPurpose`) with evidence requirement.
2. Launch security reviewer lane for high-risk paths.
3. Run build/test/lint checks; do not finalize on stale results.
4. If verification fails, enqueue follow-up tasks and loop to Phase 3.

### Phase 7: Final Completion Report
1. Create `completion-report.json` with:
   - delivered tasks
   - verification evidence
   - unresolved limitations
2. Return concise summary + risks + next actions.
3. Mark pipeline state `complete`.

## Auto Mode Guidelines
- Continue automatically through reversible steps.
- Ask user only for materially branching decisions:
  - staffing > 4 execution workers
  - destructive git operations
  - unresolved merge conflicts requiring preference
- Keep one source of truth: `.cursor/state/team/<teamId>/`.
- Never claim completion without fresh verification output.

## State Artifacts
- `config.json`: team config and constraints
- `progress.json`: lifecycle counters and phase
- `tasks/task-*.json`: decomposed work items
- `results/result-*.json`: worker outputs
- `audit-log.json`: timestamped orchestration events
- `merge-report.json`: merge decisions and conflict handling
- `completion-report.json`: final delivery record

## Completion Criteria
- All required tasks are `completed`
- No unresolved critical conflicts
- Verification lanes passed (architect + checks)
- Completion report written with limitations documented
