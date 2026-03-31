---
name: omx-ralph-init
description: >-
  Initialize a PRD (Product Requirements Document) for structured ralph-loop
  execution. Creates structured requirements that the omx-ralph skill can use
  for goal-driven iteration. Ported from OmX $ralph-init for Cursor agent use.
---
# Ralph Init (ported from OmX $ralph-init)

## Purpose

Initialize a PRD (Product Requirements Document) for structured ralph-loop execution. Creates a structured requirements document that the omx-ralph skill can use for goal-driven iteration.

## When to Use

- User wants to create a structured PRD before starting a ralph execution loop
- User needs to define acceptance criteria, goals, and constraints for a feature or project
- User wants goal-driven iteration with clear completion criteria

## When Not to Use

- User already has a clear, specific task that doesn't need a PRD — use `omx-ralph` skill directly
- User wants to plan with multi-perspective consensus — use `omx-plan` or `omx-ralplan` skill instead
- Task is a simple fix that doesn't need structured requirements

## Workflow

1. **Gather requirements** via interactive interview or from the provided description
2. **Create PRD** at `.cursor/plans/prd-{slug}.md` with:
   - Problem statement
   - Goals and non-goals
   - Acceptance criteria (testable)
   - Technical constraints
   - Implementation phases
3. **Initialize progress ledger** at `.cursor/state/ralph-progress.json`
4. **Link to Ralph** so that the `omx-ralph` skill can use the PRD as its completion criteria

### Canonical Source Contract

- Canonical PRD source of truth is `.cursor/plans/prd-{slug}.md`
- Ralph progress source of truth is `.cursor/state/ralph-progress.json`

## Tools

- **Task tool (subagent)** with `subagent_type: "explore"` — gather codebase facts for requirements context
- **Task tool (subagent)** with `subagent_type: "generalPurpose"` — delegate requirements analysis
- **Shell tool** — create directories, check existing artifacts
- **Write tool** — create PRD and progress ledger files
- **Read tool** — read existing plans or codebase files for context

## Completion Criteria

A structured PRD file saved to `.cursor/plans/` that serves as the definition of done for Ralph execution.

## Next Steps

After creating the PRD, start execution with the `omx-ralph` skill:
```
Invoke omx-ralph with: "implement the PRD"
```

Ralph will iterate until all acceptance criteria in the PRD are met and architect-verified.
