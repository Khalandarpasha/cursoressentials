---
name: omx-ralplan
description: >-
  Alias for omx-plan --consensus. Triggers iterative planning with Planner,
  Architect, and Critic subagents until consensus is reached, with RALPLAN-DR
  structured deliberation. Ported from OmX $ralplan for Cursor agent use.
---
# Ralplan — Consensus Planning (ported from OmX $ralplan)

## Purpose

Ralplan is a shorthand alias for `omx-plan --consensus`. It triggers iterative planning with Planner, Architect, and Critic subagents until consensus is reached, with **RALPLAN-DR structured deliberation** (short mode by default, deliberate mode for high-risk work).

## When to Use

- User says "ralplan" or "consensus plan"
- Task benefits from multi-perspective validation before execution
- High-stakes projects where planner/architect/critic agreement is valuable
- User wants structured deliberation with explicit decision records

## When Not to Use

- Simple, well-scoped tasks that don't need consensus planning — just execute directly
- User wants autonomous execution without planning — use `omx-ralph` skill
- User wants a basic plan without the full consensus loop — use `omx-plan` skill in direct mode

## Rules

- Default to concise, evidence-dense progress and completion reporting unless the user or risk level requires more detail
- Treat newer user task updates as local overrides for the active workflow branch while preserving earlier non-conflicting constraints
- If correctness depends on additional inspection, retrieval, execution, or verification, keep using the relevant tools until the consensus-planning flow is grounded
- Right-size implementation steps and PRD story counts to the actual scope; do not default to exactly five steps when the task is clearly smaller or larger
- Continue through clear, low-risk, reversible next steps automatically; ask only when the next step is materially branching, destructive, or preference-dependent

## Workflow

This skill invokes the `omx-plan` skill in consensus mode.

### Flags

- `--interactive`: Enables user prompts at key decision points (draft review and final approval). Without this flag the workflow runs fully automated and outputs the final plan without asking for confirmation.
- `--deliberate`: Forces deliberate mode for high-risk work. Adds pre-mortem (3 scenarios) and expanded test planning (unit/integration/e2e/observability). Without this flag, deliberate mode can still auto-enable when the request explicitly signals high risk.

### Pre-context Intake

Before consensus planning or execution handoff, ensure a grounded context snapshot exists:

1. Derive a task slug from the request
2. Reuse the latest relevant snapshot when available
3. If none exists, create a context snapshot with: task statement, desired outcome, known facts/evidence, constraints, unknowns/open questions, likely codebase touchpoints
4. If ambiguity remains high, gather brownfield facts first using Task tool (explore subagent), then run `omx-deep-interview` skill in quick mode before continuing

Do not hand off to execution modes until intake is complete; if urgency forces progress, explicitly document the risk tradeoffs.

### Consensus Workflow

1. **Planner** creates initial plan and a compact **RALPLAN-DR summary** before review:
   - Principles (3-5)
   - Decision Drivers (top 3)
   - Viable Options (>=2) with bounded pros/cons
   - If only one viable option remains, explicit invalidation rationale for alternatives
   - Deliberate mode only: pre-mortem (3 scenarios) + expanded test plan (unit/integration/e2e/observability)
2. **User feedback** *(--interactive only)*: Present the draft plan plus the Principles / Drivers / Options summary before review (Proceed to review / Request changes / Skip review). Otherwise, automatically proceed to review.
3. **Architect** reviews for architectural soundness via Task tool (subagent) and must provide the strongest steelman antithesis, at least one real tradeoff tension, and (when possible) synthesis — **await completion before step 4**. In deliberate mode, Architect should explicitly flag principle violations.
4. **Critic** evaluates against quality criteria via Task tool (subagent) — run only after step 3 completes. Critic must enforce principle-option consistency, fair alternatives, risk mitigation clarity, testable acceptance criteria, and concrete verification steps. In deliberate mode, Critic must reject missing/weak pre-mortem or expanded test plan.
5. **Re-review loop** (max 5 iterations): Any non-APPROVE Critic verdict (ITERATE or REJECT) MUST run the same full closed loop:
   a. Collect Architect + Critic feedback
   b. Revise the plan with Planner
   c. Return to Architect review
   d. Return to Critic evaluation
   e. Repeat until Critic returns APPROVE or 5 iterations reached
   f. If 5 iterations reached without APPROVE, present the best version to the user
6. On Critic approval *(--interactive only)*: Present the plan with approval options (Approve and execute via omx-ralph / Approve and implement via Task tool with parallel subagents / Request changes / Reject). Final plan must include ADR (Decision, Drivers, Alternatives considered, Why chosen, Consequences, Follow-ups). Otherwise, output the final plan and stop.
7. *(--interactive only)* User chooses: Approve (ralph or team), Request changes, or Reject
8. *(--interactive only)* On approval: invoke `omx-ralph` skill for sequential execution or Task tool with parallel subagents for parallel team execution — never implement directly

> **Important:** Steps 3 and 4 MUST run sequentially. Do NOT issue both agent calls in the same parallel batch. Always await the Architect result before invoking Critic.

Follow the `omx-plan` skill's full documentation for consensus mode details.

### Pre-Execution Gate

Execution modes spin up heavy multi-agent orchestration. When launched on a vague request, agents have no clear target — they waste cycles on scope discovery that should happen during planning.

The ralplan-first gate intercepts underspecified execution requests and redirects them through the ralplan consensus planning workflow. This ensures:
- **Explicit scope**: A PRD defines exactly what will be built
- **Test specification**: Acceptance criteria are testable before code is written
- **Consensus**: Planner, Architect, and Critic agree on the approach
- **No wasted execution**: Agents start with a clear, bounded task

**Passes the gate** (specific enough for direct execution):
- "fix the null check in src/hooks/bridge.ts:326"
- "implement issue #42"
- "add validation to function processKeywordDetector"

**Gated — redirected to ralplan** (needs scoping first):
- "fix this"
- "build the app"
- "improve performance"
- "add authentication"

## Tools

- **Task tool (subagent)** with `subagent_type: "generalPurpose"` — delegate to planner, architect, and critic roles
- **Task tool (subagent)** with `subagent_type: "explore"` — codebase exploration during pre-context intake
- **Grep tool** — search codebase for patterns and symbols during planning
- **Read tool** — read existing plans and codebase files
- **Shell tool** — run verification commands

## Examples

**Good:** The user says `continue` after the workflow already has a clear next step. Continue the current branch of work instead of restarting or re-asking the same question.

**Good:** The user changes only the output shape or downstream delivery step (for example "make a PR"). Preserve earlier non-conflicting workflow constraints and apply the update locally.

**Bad:** The user says `continue`, and the workflow restarts discovery or stops before the missing verification/evidence is gathered.
