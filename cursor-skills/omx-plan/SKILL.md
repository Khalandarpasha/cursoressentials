---
name: omx-plan
description: >-
  Strategic planning with optional interview workflow, consensus mode
  (Planner/Architect/Critic loop with RALPLAN-DR structured deliberation),
  and review mode. Ported from OmX $plan for Cursor agent use.
---
# Plan (ported from OmX $plan)

## Purpose

Plan creates comprehensive, actionable work plans through intelligent interaction. It auto-detects whether to interview the user (broad requests) or plan directly (detailed requests), and supports consensus mode (iterative Planner/Architect/Critic loop with RALPLAN-DR structured deliberation) and review mode (Critic evaluation of existing plans).

## When to Use

- User wants to plan before implementing — "plan this", "plan the", "let's plan"
- User wants structured requirements gathering for a vague idea
- User wants an existing plan reviewed — "review this plan", `--review`
- User wants multi-perspective consensus on a plan — `--consensus`, "ralplan"
- Task is broad or vague and needs scoping before any code is written

## When Not to Use

- User wants autonomous end-to-end execution — use `omx-autopilot` skill instead
- User wants to start coding immediately with a clear task — use `omx-ralph` skill or delegate to executor
- User asks a simple question that can be answered directly — just answer it
- Task is a single focused fix with obvious scope — skip planning, just do it

## Why This Matters

Jumping into code without understanding requirements leads to rework, scope creep, and missed edge cases. Plan provides structured requirements gathering, expert analysis, and quality-gated plans so that execution starts from a solid foundation. The consensus mode adds multi-perspective validation for high-stakes projects.

## Rules

- Auto-detect interview vs direct mode based on request specificity
- Ask one question at a time during interviews — never batch multiple questions
- Gather codebase facts via Task tool (explore subagent) before asking the user about them
- Plans must meet quality standards: 80%+ claims cite file/line, 90%+ criteria are testable
- Implementation step count must be right-sized to task scope; avoid defaulting to exactly five steps when the work is clearly smaller or larger
- Consensus mode outputs the final plan by default; add `--interactive` to enable execution handoff
- Consensus mode uses RALPLAN-DR short mode by default; switch to deliberate mode with `--deliberate` or when the request explicitly signals high risk (auth/security, data migration, destructive/irreversible changes, production incident, compliance/PII, public API breakage)
- Default to concise, evidence-dense progress and completion reporting
- Continue through clear, low-risk, reversible next steps automatically; ask only when the next step is materially branching, destructive, or preference-dependent

## Workflow

### Mode Selection

| Mode | Trigger | Behavior |
|------|---------|----------|
| Interview | Default for broad requests | Interactive requirements gathering |
| Direct | `--direct`, or detailed request | Skip interview, generate plan directly |
| Consensus | `--consensus`, "ralplan" | Planner -> Architect -> Critic loop until agreement with RALPLAN-DR structured deliberation (short by default, `--deliberate` for high-risk); outputs plan by default |
| Consensus Interactive | `--consensus --interactive` | Same as Consensus but pauses for user feedback at draft and approval steps, then hands off to execution |
| Review | `--review`, "review this plan" | Critic evaluation of existing plan |

### Interview Mode (broad/vague requests)

1. **Classify the request**: Broad (vague verbs, no specific files, touches 3+ areas) triggers interview mode
2. **Ask one focused question** for preferences, scope, and constraints
3. **Gather codebase facts first**: Before asking "what patterns does your code use?", use a Task tool (explore subagent) to find out, then ask informed follow-up questions
4. **Build on answers**: Each question builds on the previous answer
5. **Consult analyst** via Task tool (subagent) for hidden requirements, edge cases, and risks
6. **Create plan** when the user signals readiness: "create the plan", "I'm ready", "make it a work plan"

### Direct Mode (detailed requests)

1. **Quick Analysis**: Optional brief analyst consultation via Task tool (subagent)
2. **Create plan**: Generate comprehensive work plan immediately
3. **Review** (optional): Critic review if requested

### Consensus Mode (`--consensus` / "ralplan")

**RALPLAN-DR modes**: **Short** (default, bounded structure) and **Deliberate** (for `--deliberate` or explicit high-risk requests). Both modes keep the same Planner -> Architect -> Critic sequence. The workflow auto-proceeds through planning steps but outputs the final plan without executing.

1. **Planner** creates initial plan and a compact **RALPLAN-DR summary** before any Architect review. The summary **MUST** include:
   - **Principles** (3-5)
   - **Decision Drivers** (top 3)
   - **Viable Options** (>=2) with bounded pros/cons for each option
   - If only one viable option remains, an explicit **invalidation rationale** for the alternatives that were rejected
   - In **deliberate mode**: a **pre-mortem** (3 failure scenarios) and an **expanded test plan** covering **unit / integration / e2e / observability**
2. **User feedback** *(--interactive only)*: Present the draft plan plus the RALPLAN-DR Principles / Decision Drivers / Options summary for early direction alignment with options: Proceed to review, Request changes, Skip review. If NOT `--interactive`, automatically proceed to review.
3. **Architect** reviews for architectural soundness via Task tool (subagent). Architect review **MUST** include: strongest steelman counterargument (antithesis), at least one meaningful tradeoff tension, and (when possible) a synthesis path. In deliberate mode, Architect should explicitly flag principle violations. **Wait for this step to complete before proceeding to step 4.** Do NOT run steps 3 and 4 in parallel.
4. **Critic** evaluates against quality criteria via Task tool (subagent). Critic **MUST** verify principle-option consistency, fair alternative exploration, risk mitigation clarity, testable acceptance criteria, and concrete verification steps. Critic **MUST** explicitly reject shallow alternatives, driver contradictions, vague risks, or weak verification. In deliberate mode, Critic **MUST** reject missing/weak pre-mortem or missing/weak expanded test plan. Run only after step 3 is complete.
5. **Re-review loop** (max 5 iterations): If Critic rejects or iterates, execute this closed loop:
   a. Collect all feedback from Architect + Critic
   b. Pass feedback to Planner to produce a revised plan
   c. **Return to Step 3** — Architect reviews the revised plan
   d. **Return to Step 4** — Critic evaluates the revised plan
   e. Repeat until Critic approves OR max 5 iterations reached
   f. If max iterations reached without approval, present the best version to the user
6. **Apply improvements**: When reviewers approve with improvement suggestions, merge all accepted improvements into the plan. Final consensus output **MUST** include an **ADR** section with: **Decision**, **Drivers**, **Alternatives considered**, **Why chosen**, **Consequences**, **Follow-ups**.
7. On Critic approval *(--interactive only)*: Present the plan with options: Approve and execute (via omx-ralph skill), Approve and implement via Task tool with parallel subagents, Request changes, Reject. If NOT `--interactive`, output the final approved plan and stop. Do NOT auto-execute.
8. *(--interactive only)* On user approval:
   - **Approve and execute**: Invoke `omx-ralph` skill with the approved plan as context. Do NOT implement directly in the planning agent.
   - **Approve and implement via team**: Invoke Task tool with parallel subagents with the approved plan as context. Do NOT implement directly.

### Review Mode (`--review`)

0. Treat review as a reviewer-only pass. The context that wrote the plan MUST NOT be the context that approves it.
1. Read the plan file
2. Evaluate via Task tool (subagent) acting as critic
3. For cleanup/refactor work, verify that the artifact includes a cleanup plan, regression tests or an explicit test gap, smell-by-smell passes, and quality gates
4. Return verdict: APPROVED, REVISE (with specific feedback), or REJECT (replanning required)

### Plan Output Format

Every plan includes:
- Requirements Summary
- Acceptance Criteria (testable)
- Implementation Steps (with file references)
- Adaptive step count sized to the actual scope (not a fixed five-step template)
- Risks and Mitigations
- Verification Steps
- For consensus/ralplan: **RALPLAN-DR summary** (Principles, Decision Drivers, Options)
- For consensus/ralplan final output: **ADR** (Decision, Drivers, Alternatives considered, Why chosen, Consequences, Follow-ups)
- For deliberate consensus mode: **Pre-mortem (3 scenarios)** and **Expanded Test Plan** (unit/integration/e2e/observability)

Plans are saved to `.cursor/plans/`. Drafts go to `.cursor/drafts/`.

## Tools

- **Task tool (subagent)** with `subagent_type: "explore"` — gather codebase facts before asking the user
- **Task tool (subagent)** with `subagent_type: "generalPurpose"` — delegate to planner, architect, analyst, and critic roles for planning validation, requirements analysis, and plan review
- **Grep tool** — search codebase for patterns, symbols, and references during planning
- **Read tool** — read existing plans and codebase files
- **Shell tool** — run verification commands

**CRITICAL — Consensus mode agent calls MUST be sequential, never parallel.** Always await the Architect result before issuing the Critic call.

## Examples

**Good — Adaptive interview (gathering facts before asking):**
```
Planner: [uses Task explore subagent: "find authentication implementation"]
Planner: [receives: "Auth is in src/auth/ using JWT with passport.js"]
Planner: "I see you're using JWT authentication with passport.js in src/auth/.
         For this new feature, should we extend the existing auth or add a separate auth flow?"
```
Why good: Answers its own codebase question first, then asks an informed preference question.

**Good — Single question at a time:**
```
Q1: "What's the main goal?"
A1: "Improve performance"
Q2: "For performance, what matters more — latency or throughput?"
A2: "Latency"
Q3: "For latency, are we optimizing for p50 or p99?"
```
Why good: Each question builds on the previous answer. Focused and progressive.

**Bad — Asking about things you could look up:**
```
Planner: "Where is authentication implemented in your codebase?"
User: "Uh, somewhere in src/auth I think?"
```
Why bad: The planner should use a Task explore subagent to find this, not ask the user.

**Bad — Batching multiple questions:**
```
"What's the scope? And the timeline? And who's the audience?"
```
Why bad: Three questions at once causes shallow answers. Ask one at a time.

## Checklist

- [ ] Plan has testable acceptance criteria (90%+ concrete)
- [ ] Plan references specific files/lines where applicable (80%+ claims)
- [ ] All risks have mitigations identified
- [ ] No vague terms without metrics ("fast" -> "p99 < 200ms")
- [ ] Plan saved to `.cursor/plans/`
- [ ] In consensus mode: RALPLAN-DR summary includes 3-5 principles, top 3 drivers, and >=2 viable options (or explicit invalidation rationale)
- [ ] In consensus mode final output: ADR section included (Decision / Drivers / Alternatives considered / Why chosen / Consequences / Follow-ups)
- [ ] In deliberate consensus mode: pre-mortem (3 scenarios) + expanded test plan (unit/integration/e2e/observability) included
- [ ] In consensus mode with `--interactive`: user explicitly approved before any execution; without `--interactive`: output final plan after Critic approval (no auto-execution)

## Appendix

### Design Option Presentation

When presenting design choices during interviews, chunk them:

1. **Overview** (2-3 sentences)
2. **Option A** with trade-offs
3. [Wait for user reaction]
4. **Option B** with trade-offs
5. [Wait for user reaction]
6. **Recommendation** (only after options discussed)

Format for each option:
```
### Option A: [Name]
**Approach:** [1 sentence]
**Pros:** [bullets]
**Cons:** [bullets]

What's your reaction to this approach?
```

### Question Classification

Before asking any interview question, classify it:

| Type | Examples | Action |
|------|----------|--------|
| Codebase Fact | "What patterns exist?", "Where is X?" | Explore first, do not ask user |
| User Preference | "Priority?", "Timeline?" | Ask user |
| Scope Decision | "Include feature Y?" | Ask user |
| Requirement | "Performance constraints?" | Ask user |

### Review Quality Criteria

| Criterion | Standard |
|-----------|----------|
| Clarity | 80%+ claims cite file/line |
| Testability | 90%+ criteria are concrete |
| Verification | All file refs exist |
| Specificity | No vague terms |
