---
name: omx-ralph
description: >-
  Self-referential persistence loop that keeps working on a task until fully
  complete and architect-verified, with parallel execution, automatic retry,
  and mandatory verification. Ported from OmX $ralph for Cursor agent use.
---
# Ralph (ported from OmX $ralph)

## Purpose

Ralph is a persistence loop that keeps working on a task until it is fully complete and architect-verified. It wraps parallel execution with session persistence, automatic retry on failure, and mandatory verification before completion.

## When to Use

- Task requires guaranteed completion with verification (not just "do your best")
- User says "ralph", "don't stop", "must complete", "finish this", or "keep going until done"
- Work may span multiple iterations and needs persistence across retries
- Task benefits from parallel execution with architect sign-off at the end

## When Not to Use

- User wants a full autonomous pipeline from idea to code — use `omx-autopilot` skill instead
- User wants to explore or plan before committing — use `omx-plan` skill instead
- User wants a quick one-shot fix — delegate directly to an executor agent
- User wants manual control over completion — use parallel Task subagents directly

## Why This Matters

Complex tasks often fail silently: partial implementations get declared "done", tests get skipped, edge cases get forgotten. Ralph prevents this by looping until work is genuinely complete, requiring fresh verification evidence before allowing completion, and using tiered architect review to confirm quality.

## Rules

- Fire independent agent calls simultaneously — never wait sequentially for independent work
- Use background execution for long operations (installs, builds, test suites)
- Deliver the full implementation: no scope reduction, no partial completion, no deleting tests to make them pass
- Default to concise, evidence-dense progress and completion reporting
- Treat newer user task updates as local overrides for the active workflow branch while preserving earlier non-conflicting constraints
- If correctness depends on additional inspection, retrieval, execution, or verification, keep using the relevant tools until the execution loop is grounded
- Continue through clear, low-risk, reversible next steps automatically; ask only when the next step is materially branching, destructive, or preference-dependent

## Workflow

### 0. Pre-context Intake (required before execution loop starts)

- Assemble or load a context snapshot with:
  - Task statement
  - Desired outcome
  - Known facts/evidence
  - Constraints
  - Unknowns/open questions
  - Likely codebase touchpoints
- If request ambiguity is high, gather brownfield facts first using Task tool (explore subagent), then run `omx-deep-interview` skill in quick mode to close critical gaps.
- Do not begin Ralph execution work until snapshot grounding exists.

### 1. Review Progress

Check TODO list and any prior iteration state.

### 2. Continue From Where You Left Off

Pick up incomplete tasks.

### 3. Delegate in Parallel

Route tasks to specialist subagents at appropriate levels:
- Simple lookups: fast model Task subagent — "What does this function return?"
- Standard work: default Task subagent — "Add error handling to this module"
- Complex analysis: thorough Task subagent — "Debug this race condition"
- When entered as a ralplan follow-up, start from the approved agent roster and make the delegation plan explicit: implementation lane, evidence/regression lane, and final sign-off lane

### 4. Run Long Operations in Background

Builds, installs, test suites use `block_until_ms: 0` on the Shell tool.

### 5. Visual Task Gate (when screenshot/reference images are present)

- Run visual verification before every next edit
- Require structured feedback: score, verdict, category match, differences, suggestions, reasoning
- Default pass threshold: score >= 90

### 6. Verify Completion with Fresh Evidence

a. Identify what command proves the task is complete
b. Run verification (test, build, lint) via Shell tool
c. Read the output — confirm it actually passed
d. Check: zero pending/in_progress TODO items

### 7. Architect Verification (tiered)

- <5 files, <100 lines with full tests: standard Task subagent (architect role)
- Standard changes: standard Task subagent (architect role)
- >20 files or security/architectural changes: thorough Task subagent (architect role)
- Ralph floor: always at least standard-tier, even for small changes

### 7.5. Regression Re-verification

- After verification passes, re-run all tests/build/lint via Shell tool and read the output to confirm they still pass
- If regression fails, fix and retry until green
- Do not proceed to completion until regression is green

### 8. On Approval

Clean exit — mark all state as complete.

### 9. On Rejection

Fix the issues raised, then re-verify at the same tier.

## Tools

- **Task tool (subagent)** with `subagent_type: "generalPurpose"` — delegate implementation, analysis, and architect verification to specialist subagents
- **Task tool (subagent)** with `subagent_type: "explore"` — codebase exploration and fact-gathering
- **Shell tool** — run builds, tests, lint, and other verification commands (use `block_until_ms: 0` for long operations)
- **StrReplace tool** — apply code edits
- **ReadLints tool** — check for linter errors on affected files
- **Grep tool** — search codebase for patterns and symbols
- **Read tool** — read files for context and verification output

## Examples

**Good — Correct parallel delegation:**
```
Task subagent 1: "Add type export for UserConfig" (fast model)
Task subagent 2: "Implement the caching layer for API responses" (default)
Task subagent 3: "Refactor auth module to support OAuth2 flow" (thorough)
```
Why good: Three independent tasks fired simultaneously at appropriate tiers.

**Good — Correct verification before completion:**
```
1. Shell: npm test           → Output: "42 passed, 0 failed"
2. Shell: npm run build      → Output: "Build succeeded"
3. ReadLints tool            → Output: 0 errors
4. Task subagent architect   → Verdict: "APPROVED"
5. Clean exit
```
Why good: Fresh evidence at each step, architect verification, then clean exit.

**Bad — Claiming completion without verification:**
"All the changes look good, the implementation should work correctly. Task complete."
Why bad: Uses "should" and "look good" — no fresh test/build output, no architect verification.

**Bad — Sequential execution of independent tasks:**
```
Task subagent 1: "Add type export" → wait →
Task subagent 2: "Implement caching" → wait →
Task subagent 3: "Refactor auth"
```
Why bad: These are independent tasks that should run in parallel, not sequentially.

## Completion Criteria

- Stop and report when a fundamental blocker requires user input (missing credentials, unclear requirements, external service down)
- Stop when the user says "stop", "cancel", or "abort"
- If architect rejects verification, fix the issues and re-verify (do not stop)
- If the same issue recurs across 3+ iterations, report it as a potential fundamental problem

## Checklist

- [ ] All requirements from the original task are met (no scope reduction)
- [ ] Zero pending or in_progress TODO items
- [ ] Fresh test run output shows all tests pass
- [ ] Fresh build output shows success
- [ ] ReadLints tool shows 0 errors on affected files
- [ ] Architect verification passed (standard tier minimum)
- [ ] Post-verification regression tests pass
- [ ] Clean state on exit

## Appendix

### PRD Mode (Optional)

When the user provides the `--prd` flag, initialize a Product Requirements Document before starting the ralph loop.

**PRD Workflow:**
1. Run `omx-deep-interview` skill in quick mode before creating PRD artifacts
2. Create canonical PRD at `.cursor/plans/prd-{slug}.md`
3. Create progress ledger at `.cursor/state/ralph-progress.json`
4. Parse the task and break down into user stories with acceptance criteria
5. Proceed to normal ralph loop using user stories as the task list

After creating the PRD, Ralph will iterate until all acceptance criteria in the PRD are met and architect-verified.

### Background Execution Rules

**Run in background** (`block_until_ms: 0` on Shell tool):
- Package installation (npm install, pip install, cargo build)
- Build processes (make, project build commands)
- Test suites
- Docker operations (docker build, docker pull)

**Run blocking** (foreground):
- Quick status checks (git status, ls, pwd)
- File reads and edits
- Simple commands
