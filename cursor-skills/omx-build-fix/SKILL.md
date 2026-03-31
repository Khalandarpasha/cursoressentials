---
name: omx-build-fix
description: >-
  Fix build and TypeScript errors with minimal changes. Get the build green
  without refactoring.
---
# Build Fix (ported from OmX $build-fix)

## Purpose

Fix build and compilation errors quickly with minimal code changes. Get the build green without refactoring.

## When to Use

- User says "fix the build", "build is broken"
- TypeScript compilation fails
- The build command or type checker reports errors
- User requests "minimal fixes" for errors

## When Not to Use

- User wants a refactor or architectural improvement
- The issue is a runtime bug, not a build/compile error
- User wants performance optimization

## Rules

- Default to concise, evidence-dense progress and completion reporting unless the user or risk level requires more detail.
- Treat newer user task updates as local overrides for the active workflow branch while preserving earlier non-conflicting constraints.
- If correctness depends on additional inspection, retrieval, execution, or verification, keep using the relevant tools until the build-fix workflow is grounded.
- Continue through clear, low-risk, reversible next steps automatically; ask only when the next step is materially branching, destructive, or preference-dependent.

## Workflow

1. **Collect Errors**
   - Run the project's type check command (e.g., `tsc --noEmit`, `mypy`, `cargo check`, `go vet`) using `Shell tool`
   - Or run the project's build command to get build failures
   - Use `ReadLints tool` to collect diagnostic errors
   - Categorize errors by type and severity

2. **Fix Strategically**
   - Add type annotations where missing
   - Add null checks where needed
   - Fix import/export statements
   - Resolve module resolution issues
   - Fix linter errors blocking build

3. **Minimal Diff Strategy**
   - NO refactoring of unrelated code
   - NO architectural changes
   - NO performance optimizations
   - ONLY what's needed to make build pass

4. **Verify**
   - Run the project's type check command after each fix using `Shell tool`
   - Use `ReadLints tool` to check for remaining errors
   - Ensure no new errors introduced
   - Stop when build passes

## Tools

- **Shell tool** — run build, typecheck, lint, and test commands
- **ReadLints tool** — collect and verify diagnostic/linter errors
- **StrReplace tool** — make minimal targeted code fixes
- **Grep tool** — search for error-related patterns and symbols
- **Task tool with explore subagent** — find related files when needed

## Examples

**Good:** The user says `continue` after the workflow already has a clear next step. Continue the current branch of work instead of restarting or re-asking the same question.

**Good:** The user changes only the output shape or downstream delivery step (for example "make a PR"). Preserve earlier non-conflicting workflow constraints and apply the update locally.

**Bad:** The user says `continue`, and the workflow restarts discovery or stops before the missing verification/evidence is gathered.

## Output Format

```text
BUILD FIX REPORT
================

Errors Fixed: 12
Files Modified: 8
Lines Changed: 47

Fixes Applied:
1. src/utils/validation.ts:15 - Added return type annotation
2. src/components/Header.tsx:42 - Added null check for props.user
3. src/api/client.ts:89 - Fixed import path for axios
...

Final Build Status: PASSING
Verification: [type check command] (exit code 0)
```

## Completion Criteria

The build-fix workflow stops when:
- Type check command exits with code 0
- Build command completes successfully
- No new errors introduced

## Checklist

- **One fix at a time** — Easier to verify and debug
- **Minimal changes** — Don't refactor while fixing
- **Document why** — Comment non-obvious fixes
- **Test after** — Ensure tests still pass
