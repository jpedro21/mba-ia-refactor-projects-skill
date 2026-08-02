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
2. **Iterate through the Phase 2 report finding-by-finding**, in order CRITICAL → HIGH → MEDIUM → LOW, and apply the matching pattern from [refactoring-playbook.md](refactoring-playbook.md). Do NOT treat "moved code into models/controllers/views/" as coverage — restructuring alone never resolves security findings.
3. Adapt structure to the detected stack (Python/Flask vs Node.js/Express).
4. Preserve all existing API endpoints and response formats.
5. Extract configuration to a `config/` module (use environment variables, no hardcoded secrets).
6. Centralize error handling in `middlewares/`.
7. Keep `app.py` or `app.js` as the composition root only.

### Anti-pattern → Refactoring Playbook map

Use this map to pick the right RP for every finding. It is exhaustive for the current catalog — if a finding does not map here, stop and update the playbook before continuing.

| Anti-pattern | Playbook pattern |
|---|---|
| AP-01 SQL Injection | RP-01 Parameterized Queries |
| AP-02 Hardcoded Credentials | RP-02 Config Module |
| AP-03 God Class / God File | RP-03 Split into MVC Layers |
| AP-04 Unrestricted Admin/Debug Endpoints | RP-04 Remove Dangerous Admin Endpoints |
| AP-05 Business Logic in Routes/Controllers | RP-05 Extract to Controller |
| **AP-06 Insecure Password Handling** | **RP-06 Secure Password Handling (hash on write, verify on read, never return in responses)** |
| AP-07 Global Mutable State | RP-07 Dependency Injection |
| AP-08 Callback Hell | RP-08 Async/Await |
| AP-09 N+1 Queries | RP-09 JOINs / Batch Queries |
| AP-11 Sensitive Data Exposure | Sanitize responses (drop secret_key, db_path, password fields, debug flags) |
| AP-12 Deprecated APIs | RP-11 Replace Deprecated APIs |
| AP-14 Magic Numbers/Strings | RP-12 Extract Constants |
| AP-16 Bare Exception Handling | RP-10 Centralized Error Handling |

### Finding coverage checklist (MANDATORY)

Before printing the completion summary, produce and print this table. It MUST include **every** CRITICAL and HIGH finding from the Phase 2 report — no exceptions, no batching, no "covered implicitly by restructuring."

```
Finding coverage:
| Severity | Finding | Anti-pattern | RP applied | File(s) modified | Status |
|----------|---------|--------------|------------|------------------|--------|
| CRITICAL | <name> | AP-XX        | RP-YY      | path/to/file.py  | done   |
| HIGH     | <name> | AP-06        | RP-06      | models/usuario_model.py, database.py | done |
| ...      | ...    | ...          | ...        | ...              | ...    |
```

Rules:
- **Every CRITICAL and HIGH finding must have `Status: done` with a concrete RP + modified file.** A CRITICAL/HIGH finding without an RP applied blocks Phase 3 completion — go back and apply it before continuing.
- MEDIUM findings are strongly encouraged; LOW findings are optional but must be listed as `skipped` if not addressed.
- If a finding was already resolved in a prior run, still list it with the file where the fix lives and `Status: verified`.

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

**Static security checks (fail Phase 3 if any of these trip):**

```bash
# 1. Password field returned in API response dicts (models/controllers only)
grep -rniE "['\"](senha|password)['\"]\s*:" models/ controllers/ | grep -viE "erro|mensagem|obrigat" || echo "(none)"
# 2. Weak hashing
grep -rniE "\bmd5\(|\bsha1\(" models/ controllers/ database.py || echo "(none)"
# 3. Login must not compare password in SQL
grep -rniE "WHERE .* (senha|password) *= *\?" models/ || echo "(none)"
# 4. Password columns must be written via a hashing helper.
#    Inspect INSERT/UPDATE statements touching senha/password *with their next 3 lines*
#    (the values tuple lives on the following line in Python). A block with no
#    hash_password/generate_password_hash/bcrypt/argon2 nearby means plaintext write.
grep -rniEA3 "INSERT INTO .*(senha|password)|UPDATE .* SET .*(senha|password)" models/ database.py \
  | awk 'BEGIN{RS="--\n"} !/hash_password|generate_password_hash|bcrypt|argon2/ && NF' \
  | grep -E "." || echo "(none)"
```

The word "senha"/"password" appearing as a column name, function parameter, or user-facing error message is fine — the checks above target concrete plaintext handling patterns instead.

For projects with a user domain, confirm the appropriate password library is imported:
- Python: `from werkzeug.security import generate_password_hash, check_password_hash` (or `bcrypt`/`argon2`).
- Node.js: `bcrypt` or `argon2`.

Print completion summary:

```
================================
PHASE 3: REFACTORING COMPLETE
================================
New Project Structure:
<tree output>

Finding coverage:
<table from checklist above>

Validation
  ✓ Application boots without errors
  ✓ All endpoints respond correctly
  ✓ All CRITICAL and HIGH findings addressed
  ✓ Static security checks pass (no plaintext passwords, no weak hashing)
================================
```

If validation fails, fix issues before declaring complete.

---

## Technology-Agnostic Rules

- **Python/Flask**: `models/` = data access, `controllers/` = business logic, `views/routes.py` = routing, `config/settings.py` = config
- **Node.js/Express**: `models/` = data access, `controllers/` = business logic, `views/routes.js` = routing, `config/settings.js` = config
- Use parameterized queries everywhere (never string concatenation for SQL).
- Never store or compare passwords in plaintext — hash on write, verify on read (RP-06). Applies to seed data too.
- Never expose passwords, secret keys, or credentials in API responses.
- Remove admin/debug endpoints that allow arbitrary SQL execution.
- Replace deprecated APIs (e.g., `datetime.utcnow()` → `datetime.now(timezone.utc)`).
