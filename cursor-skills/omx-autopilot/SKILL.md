---
name: omx-autopilot
description: >-
  Full autonomous execution from idea to working code. Takes a brief product
  idea and autonomously handles the full lifecycle: requirements analysis,
  technical design, planning, parallel implementation, QA cycling, and
  multi-perspective validation.
---
# Autopilot (ported from OmX $autopilot)

## Purpose

Autopilot takes a brief product idea and autonomously handles the full lifecycle: requirements analysis, technical design, planning, parallel implementation, QA cycling, and multi-perspective validation. It produces working, verified code from a 2-3 line description.

## When to Use

- User wants end-to-end autonomous execution from an idea to working code
- User says "autopilot", "auto pilot", "autonomous", "build me", "create me", "make me", "full auto", "handle it all", or "I want a/an..."
- Task requires multiple phases: planning, coding, testing, and validation
- User wants hands-off execution and is willing to let the system run to completion

## When Not to Use

- User wants to explore options or brainstorm — use `omx-plan skill` instead
- User says "just explain", "draft only", or "what would you suggest" — respond conversationally
- User wants a single focused code change — use `omx-ralph skill` or delegate to an executor agent
- User wants to review or critique an existing plan — use plan skill with review mode
- Task is a quick fix or small bug — use direct executor delegation

## Why This Matters

Most non-trivial software tasks require coordinated phases: understanding requirements, designing a solution, implementing in parallel, testing, and validating quality. Autopilot orchestrates all of these phases automatically so the user can describe what they want and receive working code without managing each step.

## Rules

- Each phase must complete before the next begins
- Parallel execution is used within phases where possible (Phase 2 and Phase 4)
- QA cycles repeat up to 5 times; if the same error persists 3 times, stop and report the fundamental issue
- Validation requires approval from all reviewers; rejected items get fixed and re-validated
- If a deep-interview spec exists, use it as high-clarity phase input instead of re-expanding from scratch
- If input is too vague for reliable expansion, offer/trigger `omx-deep-interview skill` first
- Do not enter expansion/planning/execution-heavy phases until pre-context grounding exists; if fast execution is forced, proceed only with explicit risk notes
- Default to concise, evidence-dense progress and completion reporting unless the user or risk level requires more detail
- Treat newer user task updates as local overrides for the active workflow branch while preserving earlier non-conflicting constraints
- If correctness depends on additional inspection, retrieval, execution, or verification, keep using the relevant tools until the workflow is grounded
- Continue through clear, low-risk, reversible next steps automatically; ask only when the next step is materially branching, destructive, or preference-dependent

## Workflow

### Phase 0 — Pre-context Intake (required)

- Derive a task slug from the request
- Load the latest relevant snapshot from `.cursor/context/{slug}-*.md` when available
- If no snapshot exists, create `.cursor/context/{slug}-{timestamp}.md` (UTC `YYYYMMDDTHHMMSSZ`) with:
  - Task statement
  - Desired outcome
  - Known facts/evidence
  - Constraints
  - Unknowns/open questions
  - Likely codebase touchpoints
- If ambiguity remains high, use `Task tool with explore subagent` first for brownfield facts, then run `omx-deep-interview skill --quick <task>` before proceeding
- Carry the snapshot path into autopilot artifacts/state so all phases share grounded context

### Phase 1 — Expansion

Turn the user's idea into a detailed spec:
- If `.cursor/specs/deep-interview-*.md` exists for this task: reuse it and skip redundant expansion work
- If prompt is highly vague: route to `omx-deep-interview skill` for Socratic ambiguity-gated clarification
- Extract requirements thoroughly
- Create technical specification
- Output: `.cursor/plans/autopilot-spec.md`

### Phase 2 — Planning

Create an implementation plan from the spec:
- Create plan (direct mode, no interview)
- Validate plan with critical review
- Output: `.cursor/plans/autopilot-impl.md`

### Phase 3 — Execution

Implement the plan:
- Simple tasks: handle directly
- Standard tasks: use focused implementation
- Complex tasks: use `Task tool with parallel subagents` for independent subtasks
- Run independent tasks in parallel

### Phase 4 — QA

Cycle until all tests pass:
- Build, lint, test, fix failures
- Repeat up to 5 cycles
- Stop early if the same error repeats 3 times (indicates a fundamental issue)

### Phase 5 — Validation

Multi-perspective review in parallel using `Task tool with parallel subagents`:
- Functional completeness review
- Security/vulnerability check
- Code quality review
- All must approve; fix and re-validate on rejection

### Phase 6 — Cleanup

Clear all state on successful completion.

## Tools

- **Task tool (subagent) with generalPurpose** — architecture validation and complex analysis
- **Task tool with parallel subagents** — parallel execution and multi-perspective validation
- **Task tool with explore subagent** — codebase search and file discovery
- **Shell tool** — run build, test, lint, typecheck commands
- **ReadLints tool** — check for linter/diagnostic errors
- **StrReplace tool** — make code edits
- **Grep tool** — search codebase for patterns and symbols

## Examples

**Good:** User: "autopilot A REST API for a bookstore inventory with CRUD operations using TypeScript"
Why good: Specific domain (bookstore), clear features (CRUD), technology constraint (TypeScript). Autopilot has enough context to expand into a full spec.

**Good:** User: "build me a CLI tool that tracks daily habits with streak counting"
Why good: Clear product concept with a specific feature. The "build me" trigger activates autopilot.

**Bad:** User: "fix the bug in the login page"
Why bad: This is a single focused fix, not a multi-phase project. Use direct executor delegation or omx-ralph skill instead.

**Bad:** User: "what are some good approaches for adding caching?"
Why bad: This is an exploration/brainstorming request. Respond conversationally or use the plan skill.

## Completion Criteria

- [ ] All phases completed (Expansion, Planning, Execution, QA, Validation)
- [ ] All validators approved in Phase 5
- [ ] Tests pass (verified with fresh test run output)
- [ ] Build succeeds (verified with fresh build output)
- [ ] State files cleaned up
- [ ] User informed of completion with summary of what was built

## Appendix

### Recommended Clarity Pipeline

For ambiguous requests, prefer:

```
omx-deep-interview -> omx-plan (consensus) -> omx-autopilot
```

- `omx-deep-interview`: ambiguity-gated Socratic requirements
- `omx-plan (consensus)`: consensus planning (planner/architect/critic)
- `omx-autopilot`: execution + QA + validation

### Best Practices for Input

1. Be specific about the domain — "bookstore" not "store"
2. Mention key features — "with CRUD", "with authentication"
3. Specify constraints — "using TypeScript", "with PostgreSQL"
4. Let it run — avoid interrupting unless truly needed

### Escalation and Stop Conditions

- Stop and report when the same QA error persists across 3 cycles (fundamental issue requiring human input)
- Stop and report when validation keeps failing after 3 re-validation rounds
- Stop when the user says "stop", "cancel", or "abort"
- If requirements were too vague and expansion produces an unclear spec, pause and redirect to `omx-deep-interview skill` before proceeding

### Troubleshooting

**Stuck in a phase?** Check the todo list for blocked tasks, or cancel and resume.

**QA cycles exhausted?** The same error 3 times indicates a fundamental issue. Review the error pattern; manual intervention may be needed.

**Validation keeps failing?** Review the specific issues. Requirements may have been too vague — cancel and provide more detail.
