---
name: omx-ultraqa
description: >-
  Autonomous QA cycling workflow — test, verify, fix, repeat until quality goal is met. Adapted for Cursor agent use.
---
# UltraQA (ported from OmX $ultraqa)

## Purpose
UltraQA is an autonomous QA cycling workflow that runs until your quality goal is met. It follows a cycle of: run QA check → diagnose failure → fix → repeat.

## When to Use
- When you need to iteratively fix failing tests, builds, lint errors, or type errors
- User says "ultraqa"
- When the goal is to get a verification command to pass through iterative fixing
- When quality enforcement requires cycling through diagnosis and repair

## When Not to Use
- For single, obvious fixes that don't need iterative cycling
- When the user just wants to run a test once without auto-fixing
- For exploratory investigation without a clear pass/fail goal

## Rules

1. **PARALLEL when possible** — Run diagnosis while preparing potential fixes
2. **TRACK failures** — Record each failure to detect patterns
3. **EARLY EXIT on pattern** — 3x same failure = stop and surface the root cause
4. **CLEAR OUTPUT** — User should always know current cycle and status
5. **CLEAN UP** — Report final state on completion or cancellation
6. Default to concise, evidence-dense progress and completion reporting
7. Continue through clear, low-risk, reversible next steps automatically; ask only when the next step is materially branching, destructive, or preference-dependent

## Workflow

### Goal Parsing

Parse the goal from the user's request. Supported goal types:

| Goal Type | What to Check |
|-----------|---------------|
| tests | All test suites pass |
| build | Build succeeds with exit 0 |
| lint | No lint errors |
| typecheck | No TypeScript/type errors |
| custom | Custom success pattern in output |

If no structured goal is provided, interpret the argument as a custom goal.

### Cycle N (Max 5)

1. **RUN QA**: Execute verification based on goal type using the Shell tool
   - tests: Run the project's test command
   - build: Run the project's build command
   - lint: Run the project's lint command
   - typecheck: Run the project's type check command
   - custom: Run appropriate command and check for pattern

2. **CHECK RESULT**: Did the goal pass?
   - **YES** → Exit with success message
   - **NO** → Continue to step 3

3. **DIAGNOSE**: Analyze failure output to identify root cause
   - Use Read tool and Grep tool to understand the failing code
   - Use ReadLints tool for lint/typecheck goals
   - Determine specific fix recommendations

4. **FIX ISSUES**: Apply the diagnosis recommendations
   - Use StrReplace tool to make targeted fixes
   - Fix only what the diagnosis identified — no unrelated changes

5. **REPEAT**: Go back to step 1

### Exit Conditions

| Condition | Action |
|-----------|--------|
| **Goal Met** | Exit with success: "ULTRAQA COMPLETE: Goal met after N cycles" |
| **Cycle 5 Reached** | Exit with diagnosis: "ULTRAQA STOPPED: Max cycles. Diagnosis: ..." |
| **Same Failure 3x** | Exit early: "ULTRAQA STOPPED: Same failure detected 3 times. Root cause: ..." |
| **Environment Error** | Exit: "ULTRAQA ERROR: [description]" |

## Tools

- **Shell tool**: Run test, build, lint, and typecheck commands for each QA cycle
- **Read tool**: Read source and test files to understand failures
- **Grep tool**: Search for patterns related to failures across the codebase
- **StrReplace tool**: Apply targeted fixes to source files
- **ReadLints tool**: Check for linter/type errors as part of QA verification
- **Task tool (subagent)**: Optionally delegate complex diagnosis to a focused subagent

## Examples

### Observability Output
```
[ULTRAQA Cycle 1/5] Running tests...
[ULTRAQA Cycle 1/5] FAILED - 3 tests failing
[ULTRAQA Cycle 1/5] Diagnosing...
[ULTRAQA Cycle 1/5] Fixing: auth.test.ts - missing mock
[ULTRAQA Cycle 2/5] Running tests...
[ULTRAQA Cycle 2/5] PASSED - All 47 tests pass
[ULTRAQA COMPLETE] Goal met after 2 cycles
```

## Completion Criteria
- The QA goal has been met (all checks pass), OR
- Max 5 cycles reached with a clear diagnosis of remaining issues, OR
- Same failure detected 3 times with root cause reported
- Final status is clearly communicated to the user
