---
name: omx-tdd
description: >-
  Test-Driven Development enforcement skill — write tests first, always. Adapted for Cursor agent use.
---
# TDD Mode (ported from OmX $tdd)

## Purpose
Enforce strict Test-Driven Development discipline: no production code without a failing test first. The discipline IS the value — shortcuts destroy the benefit.

## When to Use
- User says "tdd" or "test first"
- When building new features that benefit from test-first methodology
- When the user explicitly wants Red-Green-Refactor cycles enforced

## When Not to Use
- Quick fixes or trivial one-line changes where TDD overhead is disproportionate
- Exploratory prototyping where tests will be written after the design stabilizes
- Configuration-only changes with no testable behavior

## Rules

**NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST**

Write code before test? DELETE IT. Start over. No exceptions.

| If You See | Action |
|------------|--------|
| Code written before test | STOP. Delete code. Write test first. |
| Test passes on first run | Test is wrong. Fix it to fail first. |
| Multiple features in one cycle | STOP. One test, one feature. |
| Skipping refactor | Go back. Clean up before next feature. |

## Workflow

### 1. RED: Write Failing Test
- Write test for the NEXT piece of functionality
- Run test using the Shell tool — MUST FAIL
- If it passes, your test is wrong

### 2. GREEN: Minimal Implementation
- Write ONLY enough code to pass the test (use StrReplace tool)
- No extras. No "while I'm here."
- Run test using the Shell tool — MUST PASS

### 3. REFACTOR: Clean Up
- Improve code quality (use StrReplace tool)
- Run tests after EVERY change using the Shell tool
- Must stay green

### 4. REPEAT
- Next failing test
- Continue cycle

## Tools

- **Shell tool**: Run the project's test command to verify RED (failing) and GREEN (passing) states
- **StrReplace tool**: Write test code and minimal production implementations
- **Read tool**: Read existing test files and source files for context
- **ReadLints tool**: Check for linter errors after refactor phase
- **Grep tool**: Search for existing test patterns and conventions in the codebase

## Output Format

When guiding TDD, report each cycle:

```
## TDD Cycle: [Feature Name]

### RED Phase
Test: [test code]
Expected failure: [what error you expect]
Actual: [run result showing failure]

### GREEN Phase
Implementation: [minimal code]
Result: [run result showing pass]

### REFACTOR Phase
Changes: [what was cleaned up]
Result: [tests still pass]
```

## Completion Criteria
- All requested functionality has been implemented through Red-Green-Refactor cycles
- All tests pass
- Code has been refactored for clarity after each GREEN phase
- No production code exists without a corresponding test
