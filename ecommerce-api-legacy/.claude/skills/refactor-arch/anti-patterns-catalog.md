# Anti-Patterns Catalog

Minimum 8 anti-patterns with severity classification and detection signals.

---

## CRITICAL

### AP-01: SQL Injection via String Concatenation
**Severity:** CRITICAL
**Detection signals:**
- SQL queries built with `+`, f-strings, or `.format()` containing user input
- `"SELECT * FROM ... WHERE id = " + str(id)`
- `"INSERT INTO ... VALUES ('" + nome + "'"`
**Impact:** Full database compromise, data theft, data destruction.
**Recommendation:** Use parameterized queries (`?` placeholders or ORM).

### AP-02: Hardcoded Credentials / Secrets
**Severity:** CRITICAL
**Detection signals:**
- `SECRET_KEY = "..."`, `password = "..."`, `api_key = "pk_live_..."`
- Credentials in source files instead of environment variables
- `app.config["SECRET_KEY"] = "hardcoded-value"`
**Impact:** Credential exposure in version control, unauthorized access.
**Recommendation:** Move to `config/` module reading from `os.environ` or `.env`.

### AP-03: God Class / God File
**Severity:** CRITICAL
**Detection signals:**
- Single file >200 lines handling DB queries, business logic, AND routing
- Class with methods for unrelated domains (users + products + orders + reports)
- `AppManager` or `models.py` containing entire application logic
**Impact:** Untestable, any change risks breaking everything.
**Recommendation:** Split by domain into models/, controllers/, views/.

### AP-04: Unrestricted Admin/Debug Endpoints
**Severity:** CRITICAL
**Detection signals:**
- `/admin/query` accepting raw SQL from request body
- `/admin/reset-db` without authentication
- Debug endpoints in production code
**Impact:** Arbitrary code execution, data loss.
**Recommendation:** Remove or protect with authentication + authorization.

---

## HIGH

### AP-05: Business Logic in Routes/Controllers
**Severity:** HIGH
**Detection signals:**
- Route handlers with >30 lines of validation + business rules
- Notification logic (`print("ENVIANDO EMAIL")`) inside route handlers
- Financial calculations directly in HTTP handlers
**Impact:** Untestable business logic, tight coupling to HTTP layer.
**Recommendation:** Extract to controller/service layer.

### AP-06: Insecure Password Handling
**Severity:** HIGH
**Detection signals:**
- Passwords stored/compared in plaintext (`senha = '" + senha + "'`)
- Weak hashing: MD5, custom `badCrypto` loops
- Passwords returned in API responses (`"senha": row["senha"]`)
**Impact:** Account compromise if database is breached.
**Recommendation:** Use bcrypt/argon2, never return passwords in responses.

### AP-07: Global Mutable State
**Severity:** HIGH
**Detection signals:**
- `global db_connection` or module-level mutable variables
- `let globalCache = {}` modified across requests
- Singleton pattern without thread safety
**Impact:** Race conditions, data leaks between requests.
**Recommendation:** Use dependency injection, request-scoped connections.

### AP-08: Callback Hell / Deep Nesting
**Severity:** HIGH
**Detection signals:**
- 4+ levels of nested callbacks in Node.js
- `db.get(..., () => { db.get(..., () => { db.run(..., () => {`
**Impact:** Unreadable, error-prone, impossible to maintain.
**Recommendation:** Use async/await or Promises, extract to service functions.

---

## MEDIUM

### AP-09: N+1 Query Problem
**Severity:** MEDIUM
**Detection signals:**
- Loop over results with individual DB query per item
- `for row in rows: cursor.execute("SELECT ... WHERE id = " + str(row["id"]))`
- `User.query.get(t.user_id)` inside `for t in tasks`
**Impact:** Performance degradation with data growth.
**Recommendation:** Use JOINs, eager loading, or batch queries.

### AP-10: Missing Input Validation
**Severity:** MEDIUM
**Detection signals:**
- Route accepts `request.get_json()` without null/type checks
- No validation on path parameters
- Missing required field checks before DB operations
**Impact:** Unexpected errors, potential data corruption.
**Recommendation:** Add validation layer (schemas, validators).

### AP-11: Sensitive Data Exposure in Responses
**Severity:** MEDIUM
**Detection signals:**
- Health check returning `secret_key`, `db_path`, `debug: true`
- User endpoints returning password hashes
- Logging credit card numbers: `console.log(card)`
**Impact:** Information disclosure to attackers.
**Recommendation:** Sanitize all API responses, never log sensitive data.

### AP-12: Deprecated API Usage
**Severity:** MEDIUM
**Detection signals:**
- Python: `datetime.utcnow()` (deprecated in 3.12+)
- Node.js: `new Buffer()` instead of `Buffer.from()`
- Flask: `@app.before_first_request` (removed in 3.0)
- Express: `bodyParser` standalone instead of `express.json()`
**Impact:** Breaks on framework upgrades.
**Recommendation:** Use modern equivalents documented in framework migration guides.

---

## LOW

### AP-13: Print-Based Logging
**Severity:** LOW
**Detection signals:**
- `print("ERRO: " + str(e))` instead of `logging.error()`
- `console.log()` for application events
**Impact:** No log levels, no structured output, lost in production.
**Recommendation:** Use `logging` module (Python) or structured logger (Node.js).

### AP-14: Magic Numbers / Strings
**Severity:** LOW
**Detection signals:**
- Hardcoded thresholds: `if faturamento > 10000`, `if priority < 1 or priority > 5`
- Status strings repeated: `"pendente"`, `"aprovado"` without constants
- Port numbers, timeouts without named constants
**Impact:** Hard to maintain, easy to introduce inconsistencies.
**Recommendation:** Extract to constants or enums in config module.

### AP-15: Poor Variable Naming
**Severity:** LOW
**Detection signals:**
- Single-letter variables: `u`, `e`, `p`, `cc`, `cid`
- Abbreviated request fields: `usr`, `eml`, `pwd`, `c_id`
**Impact:** Reduced readability, onboarding friction.
**Recommendation:** Use descriptive names matching domain language.

### AP-16: Bare Exception Handling
**Severity:** LOW
**Detection signals:**
- `except:` without exception type
- `except Exception as e:` that swallows and returns generic error
- Empty catch blocks
**Impact:** Hidden bugs, difficult debugging.
**Recommendation:** Catch specific exceptions, log details, return meaningful errors.
