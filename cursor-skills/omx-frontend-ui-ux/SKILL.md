---
name: omx-frontend-ui-ux
description: >-
  Designer-developer agent for UI/UX work including component design,
  responsive layouts, design system consistency, and accessibility compliance.
  Ported from OmX $frontend-ui-ux for Cursor agent use.
---
# Frontend UI/UX (ported from OmX $frontend-ui-ux)

## Purpose

Routes to a designer agent for frontend UI/UX work including component design, implementation, responsive layouts, design system consistency, and accessibility compliance.

## When to Use

- User needs component design and implementation
- User needs responsive layout work
- User needs design system consistency review or updates
- User needs accessibility compliance work
- Any frontend visual or interaction design task

## When Not to Use

- Backend-only tasks with no UI component
- Pure data/logic work with no visual output
- Infrastructure or DevOps tasks

## Workflow

1. Analyze the design task requirements
2. Use a Task tool (subagent) with `subagent_type: "generalPurpose"` for complex design analysis, or handle directly for straightforward UI changes
3. Implement component design and layout changes using the StrReplace tool
4. Verify accessibility and responsiveness

## Tools

- **Task tool (subagent)** with `subagent_type: "generalPurpose"` — delegate complex design analysis or multi-file UI refactoring
- **StrReplace tool** — edit component files for UI changes
- **Shell tool** — run builds, linters, or dev servers to verify changes
- **ReadLints tool** — check for linter errors after UI edits
- **Grep tool** — search for design patterns, component usage, style references

## Capabilities

- Component design and implementation
- Responsive layouts
- Design system consistency
- Accessibility compliance
