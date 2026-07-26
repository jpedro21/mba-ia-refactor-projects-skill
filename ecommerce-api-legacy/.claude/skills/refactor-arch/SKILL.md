---
name: refactor-arch
description: >-
  Audits legacy codebases for architectural anti-patterns and refactors them to MVC.
  Use when the user invokes /refactor-arch, requests architecture audit, MVC refactoring,
  or code smell analysis on any Python/Flask or Node.js/Express project.
---

# Architecture Audit & MVC Refactoring Skill

Execute three sequential phases. **Never skip phases or combine them.**

## Reference Files

Read these before acting:

| File | Purpose |
|------|---------|
| [project-analysis.md](project-analysis.md) | Stack detection heuristics |
| [anti-patterns-catalog.md](anti-patterns-catalog.md) | Anti-patterns with detection signals |
| [audit-report-template.md](audit-report-template.md) | Phase 2 report format |
| [mvc-guidelines.md](mvc-guidelines.md) | Target MVC architecture rules |
| [refactoring-playbook.md](refactoring-playbook.md) | Transformation patterns with before/after |

---

## Phase 1 — Project Analysis

1. Scan the project root and subdirectories for source files (`.py`, `.js`, `.ts`, `.json`).
2. Detect language, framework, dependencies, domain, and current architecture using [project-analysis.md](project-analysis.md).
3. Count source files analyzed and identify DB tables/entities.
4. Print the summary in this exact format:

```
================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      <language>
Framework:     <framework + version if found>
Dependencies:  <key deps>
Domain:        <business domain description>
Architecture:  <current architecture description>
Source files:  <N> files analyzed
DB tables:     <table list>
================================
```

**Stop after Phase 1.** Do not audit or modify code yet.

---

## Phase 2 — Architecture Audit

1. Read every source file in the project.
2. Cross-reference against [anti-patterns-catalog.md](anti-patterns-catalog.md).
3. For each finding, record: severity, anti-pattern name, exact file:line range, description, impact, recommendation.
4. Order findings: CRITICAL → HIGH → MEDIUM → LOW.
5. Generate the report using [audit-report-template.md](audit-report-template.md).
6. Print the report to the user.
7. Save the report to `../../reports/audit-project-{N}.md` (relative to project root, use project number based on which project is being analyzed: code-smells-project=1, ecommerce-api-legacy=2, task-manager-api=3).

**MANDATORY:** Ask the user:

```
Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
```

**Do NOT modify any source files until the user confirms with `y` or equivalent.**

---

## Phase 3 — MVC Refactoring

Only proceed after explicit user confirmation.

1. Follow [mvc-guidelines.md](mvc-guidelines.md) for target structure.
2. Apply transformations from [refactoring-playbook.md](refactoring-playbook.md) for each finding.
3. Adapt structure to the detected stack (Python/Flask vs Node.js/Express).
4. Preserve all existing API endpoints and response formats.
5. Extract configuration to a `config/` module (use environment variables, no hardcoded secrets).
6. Centralize error handling in `middlewares/`.
7. Keep `app.py` or `app.js` as the composition root only.

### Validation (required)

After refactoring, validate:

```bash
# Python/Flask
pip install -r requirements.txt
python -c "from app import app; print('Boot OK')"
# Start server and test endpoints with curl

# Node.js/Express
npm install
node -e "require('./src/app'); console.log('Boot OK')"
# Start server and test endpoints with curl
```

Print completion summary:

```
================================
PHASE 3: REFACTORING COMPLETE
================================
New Project Structure:
<tree output>

Validation
  ✓ Application boots without errors
  ✓ All endpoints respond correctly
  ✓ Zero anti-patterns remaining
================================
```

If validation fails, fix issues before declaring complete.

---

## Technology-Agnostic Rules

- **Python/Flask**: `models/` = data access, `controllers/` = business logic, `views/routes.py` = routing, `config/settings.py` = config
- **Node.js/Express**: `models/` = data access, `controllers/` = business logic, `views/routes.js` = routing, `config/settings.js` = config
- Use parameterized queries everywhere (never string concatenation for SQL).
- Never expose passwords, secret keys, or credentials in API responses.
- Remove admin/debug endpoints that allow arbitrary SQL execution.
- Replace deprecated APIs (e.g., `datetime.utcnow()` → `datetime.now(timezone.utc)`).
