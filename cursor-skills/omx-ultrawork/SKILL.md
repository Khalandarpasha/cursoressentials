---
name: omx-ultrawork
description: >-
  Parallel execution engine for high-throughput task completion using multiple subagents simultaneously. Adapted for Cursor agent use.
---
# Ultrawork (ported from OmX $ultrawork)

## Purpose
Ultrawork is a parallel execution engine that runs multiple subagents simultaneously for independent tasks. It provides parallelism and smart routing but not persistence or verification loops — it is a component that other workflows (like omx-ralph) can layer on top of.

## When to Use
- Multiple independent tasks can run simultaneously
- User says "ulw", "ultrawork", or wants parallel execution
- You need to delegate work to multiple subagents at once
- Task benefits from concurrent execution

## When Not to Use
- Task requires guaranteed completion with verification — use omx-ralph skill instead (ralph includes ultrawork)
- Task requires a full autonomous pipeline — use omx-autopilot skill instead
- There is only one sequential task with no parallelism opportunity — work directly or delegate to a single subagent
- User needs session persistence for resume — use omx-ralph skill which adds persistence on top of ultrawork

## Why This Matters
Sequential task execution wastes time when tasks are independent. Ultrawork enables firing multiple subagents simultaneously, reducing total execution time. It is designed as a composable component that ralph and autopilot layer on top of.

## Rules

- Fire all independent Task tool calls simultaneously — never serialize independent work
- Classify tasks by both complexity and dependency to choose subagent types
- Use `run_in_background: true` for operations over ~30 seconds (installs, builds, tests)
- Run quick commands (git status, file reads, simple checks) in the foreground
- When ultrawork is invoked directly (not via ralph), apply lightweight verification only — build passes, tests pass, no new errors
- If a task fails repeatedly across retries, report the issue rather than retrying indefinitely
- Escalate to the user when tasks have unclear dependencies or conflicting requirements
- Default maximum parallel workers: 4 (unless user requests higher)
- Prevent conflicting edits by assigning disjoint file ownership per worker whenever possible
- Trigger cancellation cascade when a critical blocker invalidates sibling tasks

## Workflow

1. **Build dependency map**:
   - classify tasks as `independent`, `dependent`, or `barrier`
   - create execution waves where each wave has only independent tasks
2. **Assign file ownership**:
   - each parallel worker gets explicit file/path ownership
   - avoid overlapping ownership in the same wave
3. **Route to correct complexity**:
   - Simple lookups/definitions: Use `model: "fast"` on Task tool
   - Standard implementation: Use default Task tool subagent
   - Complex analysis/refactoring: Use Task tool with detailed prompts
4. **Fire independent tasks simultaneously**: Launch each wave in one parallel Task message
5. **Run dependent tasks sequentially**: Launch next wave only after prerequisite wave succeeds
6. **Background long operations**: Builds, installs, and test suites use `run_in_background: true` on Shell tool
7. **Cancellation protocol**:
   - if one task fails with a critical blocker, mark sibling tasks in same wave as `cancel_pending`
   - stop launching new waves until blocker is resolved
8. **Verify when all tasks complete** (lightweight):
   - Build/typecheck passes
   - Affected tests pass
   - No new errors introduced

## Dependency Classification Rules
- **Independent**: no shared files, no logical prerequisite edge
- **Dependent**: requires output artifact from another task
- **Barrier**: must complete before any downstream wave starts (e.g., schema/protocol change)

## Concurrency Guidance
- Default cap: 4 concurrent workers
- Reduce to 2 when:
  - risky refactor touching shared core modules
  - frequent merge collisions detected
- Increase above 4 only with explicit user approval

## Conflict Prevention
- Use per-wave file ownership map
- Reserve shared files for a single worker per wave
- For unavoidable overlaps, schedule those tasks in sequential waves
- Emit ownership plan in task dispatch note

## Tools

- **Task tool (subagent)**: Launch multiple subagents in parallel for independent work items. Use `subagent_type: "generalPurpose"` for implementation, `subagent_type: "explore"` for analysis/search, `subagent_type: "shell"` for command execution
- **Shell tool**: Run builds, tests, and verification commands. Use `block_until_ms: 0` for long-running operations
- **StrReplace tool**: Direct file edits for simple changes that don't warrant a subagent
- **Read tool**: Read files for context before delegating
- **ReadLints tool**: Verify no new lint errors after changes

## Examples

**Good** — Three independent tasks fired simultaneously:
```
Task(subagent_type="generalPurpose", prompt="Add missing type export for Config interface", model="fast")
Task(subagent_type="generalPurpose", prompt="Implement the /api/users endpoint with validation")
Task(subagent_type="generalPurpose", prompt="Add integration tests for the auth middleware")
```
Why good: Independent tasks at appropriate complexity levels, all fired at once.

**Good** — Correct use of background execution:
```
Shell(command="npm install && npm run build", block_until_ms=0)
Task(subagent_type="generalPurpose", prompt="Update the README with new API endpoints", model="fast")
```
Why good: Long build runs in background while short task runs in parallel.

**Bad** — Sequential execution of independent work:
```
result1 = Task("Add type export")     # wait...
result2 = Task("Implement endpoint")  # wait...
result3 = Task("Add tests")           # wait...
```
Why bad: These tasks are independent. Running them sequentially wastes time.

**Bad** — Over-engineering simple tasks:
```
Task(subagent_type="generalPurpose", prompt="Add a missing semicolon")
```
Why bad: A trivial fix doesn't need a full subagent. Use StrReplace tool directly.

## Checklist
- [ ] All parallel tasks completed
- [ ] Dependency waves executed in order
- [ ] No unresolved ownership conflicts
- [ ] Build/typecheck passes
- [ ] Affected tests pass
- [ ] No new errors introduced

## Appendix

### Relationship to Other Skills

```
omx-ralph (persistence wrapper)
 \-- includes: omx-ultrawork (this skill)
     \-- provides: parallel execution only

omx-autopilot (autonomous execution)
 \-- includes: omx-ralph
     \-- includes: omx-ultrawork (this skill)
```

Ultrawork is the parallelism layer. Ralph adds persistence and verification. Autopilot adds the full lifecycle pipeline.
