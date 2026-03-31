---
name: omx-deep-interview
description: >-
  Socratic deep interview with mathematical ambiguity gating before execution.
  Turns vague ideas into execution-ready specifications by asking targeted
  questions about intent, scope, boundaries, and decision authority.
---
# Deep Interview (ported from OmX $deep-interview)

## Purpose

Deep Interview is an intent-first Socratic clarification loop before planning or implementation. It turns vague ideas into execution-ready specifications by asking targeted questions about why the user wants a change, how far it should go, what should stay out of scope, and what the Cursor agent may decide without confirmation.

## When to Use

- The request is broad, ambiguous, or missing concrete acceptance criteria
- The user says "deep interview", "interview me", "ask me everything", "don't assume", or "ouroboros"
- The user wants to avoid misaligned implementation from underspecified requirements
- You need a requirements artifact before handing off to `omx-plan skill`, `omx-autopilot skill`, `omx-ralph skill`, or `Task tool with parallel subagents`

## When Not to Use

- The request already has concrete file/symbol targets and clear acceptance criteria
- The user explicitly asks to skip planning/interview and execute immediately
- The user asks for lightweight brainstorming only (use `omx-plan skill` instead)
- A complete PRD/plan already exists and execution should start

## Why This Matters

Execution quality is usually bottlenecked by intent clarity, not just missing implementation detail. A single expansion pass often misses why the user wants a change, where the scope should stop, which tradeoffs are unacceptable, and which decisions still require user approval. This workflow applies Socratic pressure + quantitative ambiguity scoring so orchestration modes begin with an explicit, testable, intent-aligned spec.

## Rules

- Ask ONE question per round (never batch)
- Ask about intent and boundaries before implementation detail
- Target the weakest clarity dimension each round after applying the stage-priority rules
- Treat every answer as a claim to pressure-test before moving on: the next question should usually demand evidence or examples, expose a hidden assumption, force a tradeoff or boundary, or reframe root cause vs symptom
- Do not rotate to a new clarity dimension just for coverage when the current answer is still vague; stay on the same thread until one layer deeper, one assumption clearer, or one boundary tighter
- Before crystallizing, complete at least one explicit pressure pass that revisits an earlier answer with a deeper, assumption-focused, or tradeoff-focused follow-up
- Gather codebase facts via `Task tool with explore subagent` before asking user about internals
- Always run a preflight context intake before the first interview question
- Reduce user effort: ask only the highest-leverage unresolved question, and never ask the user for codebase facts that can be discovered directly
- For brownfield work, prefer evidence-backed confirmation questions such as "I found X in Y. Should this change follow that pattern?"
- Re-score ambiguity after each answer and show progress transparently
- Do not hand off to execution while ambiguity remains above threshold unless user explicitly opts to proceed with warning
- Do not crystallize or hand off while `Non-goals` or `Decision Boundaries` remain unresolved, even if the weighted ambiguity threshold is met
- Treat early exit as a safety valve, not the default success path

### Depth Profiles

- **Quick (`--quick`)**: fast pre-PRD pass; target threshold `<= 0.30`; max rounds 5
- **Standard (default)**: full requirement interview; target threshold `<= 0.20`; max rounds 12
- **Deep (`--deep`)**: high-rigor exploration; target threshold `<= 0.15`; max rounds 20

If no flag is provided, use **Standard**.

## Workflow

### Phase 0: Preflight Context Intake

1. Parse arguments and derive a short task slug.
2. Attempt to load the latest relevant context snapshot from `.cursor/context/{slug}-*.md`.
3. If no snapshot exists, create a minimum context snapshot with:
   - Task statement
   - Desired outcome
   - Stated solution (what the user asked for)
   - Probable intent hypothesis (why they likely want it)
   - Known facts/evidence
   - Constraints
   - Unknowns/open questions
   - Decision-boundary unknowns
   - Likely codebase touchpoints
4. Save snapshot to `.cursor/context/{slug}-{timestamp}.md` (UTC `YYYYMMDDTHHMMSSZ`).

### Phase 1: Initialize

1. Parse arguments and depth profile (`--quick|--standard|--deep`).
2. Detect project context:
   - Use `Task tool with explore subagent` to classify **brownfield** (existing codebase target) vs **greenfield**.
   - For brownfield, collect relevant codebase context before questioning.
3. Announce kickoff with profile, threshold, and current ambiguity.

### Phase 2: Socratic Interview Loop

Repeat until ambiguity `<= threshold`, the pressure pass is complete, the readiness gates are explicit, the user exits with warning, or max rounds are reached.

#### 2a) Generate Next Question

Use:
- Original idea
- Prior Q&A rounds
- Current dimension scores
- Brownfield context (if any)
- Activated challenge mode injection (Phase 3)

Target the lowest-scoring dimension, but respect stage priority:
- **Stage 1 — Intent-first:** Intent, Outcome, Scope, Non-goals, Decision Boundaries
- **Stage 2 — Feasibility:** Constraints, Success Criteria
- **Stage 3 — Brownfield grounding:** Context Clarity (brownfield only)

Follow-up pressure ladder after each answer:
1. Ask for a concrete example, counterexample, or evidence signal behind the latest claim
2. Probe the hidden assumption, dependency, or belief that makes the claim true
3. Force a boundary or tradeoff: what would you explicitly not do, defer, or reject?
4. If the answer still describes symptoms, reframe toward essence / root cause before moving on

Prefer staying on the same thread for multiple rounds when it has the highest leverage.

#### 2b) Ask the Question

Present:
```
Round {n} | Target: {weakest_dimension} | Ambiguity: {score}%

{question}
```

#### 2c) Score Ambiguity

Score each weighted dimension in `[0.0, 1.0]` with justification + gap.

Greenfield: `ambiguity = 1 - (intent × 0.30 + outcome × 0.25 + scope × 0.20 + constraints × 0.15 + success × 0.10)`

Brownfield: `ambiguity = 1 - (intent × 0.25 + outcome × 0.20 + scope × 0.20 + constraints × 0.15 + success × 0.10 + context × 0.10)`

Readiness gate:
- `Non-goals` must be explicit
- `Decision Boundaries` must be explicit
- A pressure pass must be complete: at least one earlier answer has been revisited with an evidence, assumption, or tradeoff follow-up
- If either gate is unresolved, or the pressure pass is incomplete, continue interviewing even when weighted ambiguity is below threshold

#### 2d) Report Progress

Show weighted breakdown table, readiness-gate status (`Non-goals`, `Decision Boundaries`), and the next focus dimension.

#### 2e) Round Controls

- Do not offer early exit before the first explicit assumption probe and one persistent follow-up have happened
- Round 4+: allow explicit early exit with risk warning
- Soft warning at profile midpoint (e.g., round 3/6/10 depending on profile)
- Hard cap at profile `max_rounds`

### Phase 3: Challenge Modes (assumption stress tests)

Use each mode once when applicable. These are normal escalation tools, not rare rescue moves:

- **Contrarian** (round 2+ or immediately when an answer rests on an untested assumption): challenge core assumptions
- **Simplifier** (round 4+ or when scope expands faster than outcome clarity): probe minimal viable scope
- **Ontologist** (round 5+ and ambiguity > 0.25, or when the user keeps describing symptoms): ask for essence-level reframing

Track used modes to prevent repetition.

### Phase 4: Crystallize Artifacts

When threshold is met (or user exits with warning / hard cap):

1. Write interview transcript summary to `.cursor/interviews/{slug}-{timestamp}.md`
2. Write execution-ready spec to `.cursor/specs/deep-interview-{slug}.md`

Spec should include:
- Metadata (profile, rounds, final ambiguity, threshold, context type)
- Context snapshot reference/path
- Clarity breakdown table
- Intent (why the user wants this)
- Desired Outcome
- In-Scope
- Out-of-Scope / Non-goals
- Decision Boundaries (what the Cursor agent may decide without confirmation)
- Constraints
- Testable acceptance criteria
- Assumptions exposed + resolutions
- Pressure-pass findings (which answer was revisited, and what changed)
- Brownfield evidence vs inference notes for any repository-grounded confirmation questions
- Technical context findings
- Full or condensed transcript

### Phase 5: Execution Bridge

Present execution options after artifact generation using explicit handoff contracts. Treat the deep-interview spec as the current requirements source of truth.

1. **`omx-plan skill` (Recommended)** — Consensus planning from the clarified spec
2. **`omx-autopilot skill`** — Full autonomous execution from the clarified spec
3. **`omx-ralph skill`** — Persistent sequential completion pressure
4. **`Task tool with parallel subagents`** — Coordinated multi-agent execution
5. **Refine further** — Re-enter questioning to resolve remaining uncertainty

**Residual-Risk Rule:** If the interview ended via early exit, hard-cap completion, or above-threshold proceed-with-warning, explicitly preserve that residual-risk state in the handoff so the downstream skill knows it inherited a partially clarified brief.

**IMPORTANT:** Deep-interview is a requirements mode. On handoff, invoke the selected skill using the contract above. **Do NOT implement directly** inside deep-interview.

## Tools

- **Task tool with explore subagent** — codebase fact gathering and brownfield context discovery
- **Grep tool** — search for patterns, symbols, and code references
- **Read tool** — read files for context during investigation
- **Write tool** — create context snapshots, transcript, and spec artifacts

## Completion Criteria

- [ ] Preflight context snapshot exists under `.cursor/context/{slug}-{timestamp}.md`
- [ ] Ambiguity score shown each round
- [ ] Intent-first stage priority used before implementation detail
- [ ] Weakest-dimension targeting used within the active stage
- [ ] At least one explicit assumption probe happened before crystallization
- [ ] At least one persistent follow-up / pressure pass deepened a prior answer
- [ ] Challenge modes triggered at thresholds (when applicable)
- [ ] Transcript written to `.cursor/interviews/{slug}-{timestamp}.md`
- [ ] Spec written to `.cursor/specs/deep-interview-{slug}.md`
- [ ] Brownfield questions use evidence-backed confirmation when applicable
- [ ] Handoff options provided (`omx-plan`, `omx-autopilot`, `omx-ralph`, parallel subagents)
- [ ] No direct implementation performed in this mode

## Appendix

### Suggested Depth Configuration

| Profile | Threshold | Max Rounds |
|---------|-----------|------------|
| Quick | 0.30 | 5 |
| Standard | 0.20 | 12 |
| Deep | 0.15 | 20 |

### Escalation and Stop Conditions

- User says stop/cancel/abort → persist state and stop
- Ambiguity stalls for 3 rounds (+/- 0.05) → force Ontologist mode once
- Max rounds reached → proceed with explicit residual-risk warning
- All dimensions >= 0.9 → allow early crystallization even before max rounds

### Recommended 3-Stage Pipeline

```
omx-deep-interview -> omx-plan (consensus) -> omx-autopilot
```

- Stage 1 (deep-interview): clarity gate
- Stage 2 (plan): feasibility + architecture gate
- Stage 3 (autopilot): execution + QA + validation gate
