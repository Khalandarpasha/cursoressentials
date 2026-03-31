---
name: omx-code-review
description: >-
  Run a comprehensive code review for quality, security, and maintainability
  with severity-rated feedback.
---
# Code Review (ported from OmX $code-review)

## Purpose

Conduct a thorough code review for quality, security, and maintainability with severity-rated feedback.

## When to Use

- User requests "review this code", "code review"
- Before merging a pull request
- After implementing a major feature
- User wants quality assessment

## When Not to Use

- Simple refactoring with well-understood patterns
- Small, isolated changes that don't warrant a full review
- Time-critical reviews where a quick scan suffices

## Rules

- Default to concise, evidence-dense progress and completion reporting unless the user or risk level requires more detail.
- Treat newer user task updates as local overrides for the active workflow branch while preserving earlier non-conflicting constraints.
- If correctness depends on additional inspection, retrieval, execution, or verification, keep using the relevant tools until the review is grounded.
- Continue through clear, low-risk, reversible next steps automatically; ask only when the next step is materially branching, destructive, or preference-dependent.

### Cross-Validation Protocol

1. **Form your OWN review FIRST** — Complete the review independently
2. **Consult for validation** — Use `Task tool (subagent)` for cross-checking findings when needed
3. **Critically evaluate** — Never blindly adopt external findings
4. **Graceful fallback** — Never block if tools unavailable

## Workflow

1. **Identify Changes**
   - Run `git diff` using `Shell tool` to find changed files
   - Determine scope of review (specific files or entire PR)

2. **Review Categories**
   - **Security** — Hardcoded secrets, injection risks, XSS, CSRF
   - **Code Quality** — Function size, complexity, nesting depth
   - **Performance** — Algorithm efficiency, N+1 queries, caching
   - **Best Practices** — Naming, documentation, error handling
   - **Maintainability** — Duplication, coupling, testability

3. **Severity Rating**
   - **CRITICAL** — Security vulnerability (must fix before merge)
   - **HIGH** — Bug or major code smell (should fix before merge)
   - **MEDIUM** — Minor issue (fix when possible)
   - **LOW** — Style/suggestion (consider fixing)

4. **Specific Recommendations**
   - File:line locations for each issue
   - Concrete fix suggestions
   - Code examples where applicable

## Tools

- **Shell tool** — run `git diff`, `git log`, tests, and build commands
- **Grep tool** — search for patterns, secrets, security issues
- **ReadLints tool** — check for diagnostic/linter errors
- **Task tool (subagent) with generalPurpose** — cross-validate findings on complex or security-sensitive code
- **Task tool with explore subagent** — understand codebase structure and find related files

## Examples

**Good:** The user says `continue` after the workflow already has a clear next step. Continue the current branch of work instead of restarting or re-asking the same question.

**Good:** The user changes only the output shape or downstream delivery step (for example "make a PR"). Preserve earlier non-conflicting workflow constraints and apply the update locally.

**Bad:** The user says `continue`, and the workflow restarts discovery or stops before the missing verification/evidence is gathered.

## Output Format

```text
CODE REVIEW REPORT
==================

Files Reviewed: 8
Total Issues: 15

CRITICAL (0)
-----------
(none)

HIGH (3)
--------
1. src/api/auth.ts:42
   Issue: User input not sanitized before SQL query
   Risk: SQL injection vulnerability
   Fix: Use parameterized queries or ORM

2. src/components/UserProfile.tsx:89
   Issue: Password displayed in plain text in logs
   Risk: Credential exposure
   Fix: Remove password from log statements

3. src/utils/validation.ts:15
   Issue: Email regex allows invalid formats
   Risk: Accepts malformed emails
   Fix: Use proven email validation library

MEDIUM (7)
----------
...

LOW (5)
-------
...

RECOMMENDATION: REQUEST CHANGES

Critical security issues must be addressed before merge.
```

## Checklist

### Security
- [ ] No hardcoded secrets (API keys, passwords, tokens)
- [ ] All user inputs sanitized
- [ ] SQL/NoSQL injection prevention
- [ ] XSS prevention (escaped outputs)
- [ ] CSRF protection on state-changing operations
- [ ] Authentication/authorization properly enforced

### Code Quality
- [ ] Functions < 50 lines (guideline)
- [ ] Cyclomatic complexity < 10
- [ ] No deeply nested code (> 4 levels)
- [ ] No duplicate logic (DRY principle)
- [ ] Clear, descriptive naming

### Performance
- [ ] No N+1 query patterns
- [ ] Appropriate caching where applicable
- [ ] Efficient algorithms (avoid O(n²) when O(n) possible)
- [ ] No unnecessary re-renders (React/Vue)

### Best Practices
- [ ] Error handling present and appropriate
- [ ] Logging at appropriate levels
- [ ] Documentation for public APIs
- [ ] Tests for critical paths
- [ ] No commented-out code

## Completion Criteria

**APPROVE** — No CRITICAL or HIGH issues, minor improvements only
**REQUEST CHANGES** — CRITICAL or HIGH issues present
**COMMENT** — Only LOW/MEDIUM issues, no blocking concerns
