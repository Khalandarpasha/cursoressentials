---
name: omx-review
description: >-
  Reviewer-only pass for plan review and cleanup artifact review, adapted for Cursor agent use
---
# Review (ported from OmX $review)

## Purpose
Review is a shorthand alias for plan review mode. It triggers Critic evaluation of an existing plan and is intended to preserve writer/reviewer separation.

## When to Use
- When you need a reviewer-only pass on an existing plan
- When reviewing cleanup or refactor proposals
- When verifying plan quality before implementation begins

## When Not to Use
- When you need to write or author a plan (use omx-plan skill instead)
- When the review target is code rather than a plan artifact

## Workflow

1. Treat review as a reviewer-only pass. The authoring context may write the plan or cleanup proposal, but a separate reviewer context must issue the verdict.
2. Read plan file from `.cursor/plans/` (or specified path)
3. Evaluate via Critic perspective
4. For cleanup/refactor/anti-slop work, confirm the artifact includes:
   - A cleanup plan
   - Regression-test coverage or an explicit test gap
   - Bounded smell-by-smell passes
   - Quality gates
5. Return verdict: **APPROVED**, **REVISE** (with specific feedback), or **REJECT** (replanning required)

## Rules

- Never write and approve in the same context.
- If the current context authored the artifact, hand review to a separate reviewer pass using the Task tool (subagent).
- Approval must cite concrete evidence, not author claims.

## Tools

- **Read tool**: Read plan files from `.cursor/plans/` or specified paths
- **Task tool (subagent)**: Delegate to a separate reviewer subagent when writer/reviewer separation is needed
- **Grep tool**: Search for specific patterns or references in plan artifacts

## Completion Criteria
- A clear verdict (APPROVED, REVISE, or REJECT) has been issued
- Verdict cites concrete evidence from the plan artifact
- Writer/reviewer separation has been maintained
