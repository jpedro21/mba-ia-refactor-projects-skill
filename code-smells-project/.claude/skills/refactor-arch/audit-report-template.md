# Audit Report Template

Use this exact structure for Phase 2 output.

```markdown
================================
ARCHITECTURE AUDIT REPORT
================================
Project: <project-name>
Stack:   <language> + <framework>
Files:   <N> analyzed | ~<LOC> lines of code

## Summary
CRITICAL: <N> | HIGH: <N> | MEDIUM: <N> | LOW: <N>

## Findings

### [CRITICAL] <Anti-Pattern Name>
File: <path>:<start_line>-<end_line>
Description: <what was found>
Impact: <why it matters>
Recommendation: <how to fix>

### [HIGH] <Anti-Pattern Name>
File: <path>:<start_line>-<end_line>
Description: <what was found>
Impact: <why it matters>
Recommendation: <how to fix>

(... repeat for all findings, ordered CRITICAL → HIGH → MEDIUM → LOW ...)

================================
Total: <N> findings
================================
```

## Rules

1. Every finding MUST have exact file path and line numbers.
2. Findings MUST be ordered by severity (CRITICAL first).
3. Minimum 5 findings per project.
4. At least 1 CRITICAL or HIGH finding required.
5. Include deprecated API findings when applicable (AP-12).
6. Reference anti-pattern IDs from [anti-patterns-catalog.md](anti-patterns-catalog.md) when relevant.
