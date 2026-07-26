# MVC Architecture Guidelines

Target architecture for refactored projects. Adapt folder names to the detected stack.

## Layer Responsibilities

### Models (`models/`)
- Data access only: CRUD operations, queries
- ORM model definitions (SQLAlchemy) or query functions (raw SQL)
- NO HTTP concerns, NO business rules, NO validation of request data
- Use parameterized queries always

### Controllers (`controllers/`)
- Business logic and orchestration
- Input validation and transformation
- Calls models for data, returns data to views
- NO direct HTTP response formatting (return dicts/objects)
- NO route definitions

### Views (`views/`)
- Route definitions and HTTP mapping only
- Thin wrappers: parse request → call controller → format response
- Blueprint/Route registration
- NO business logic, NO direct DB access

### Config (`config/`)
- All configuration from environment variables
- `SECRET_KEY`, `DATABASE_URL`, API keys via `os.environ.get()` or `dotenv`
- Constants: status enums, validation limits, ports
- NO hardcoded secrets

### Middlewares (`middlewares/`)
- Centralized error handling
- Request logging
- Authentication/authorization (if needed)
- CORS configuration (if not in app factory)

### Entry Point (`app.py` / `app.js`)
- Application factory / composition root
- Register blueprints/routes
- Initialize database
- Start server
- Minimal code (<50 lines)

---

## Python/Flask Target Structure

```
project/
├── config/
│   └── settings.py
├── models/
│   ├── __init__.py
│   ├── produto_model.py
│   └── usuario_model.py
├── controllers/
│   ├── __init__.py
│   ├── produto_controller.py
│   └── usuario_controller.py
├── views/
│   └── routes.py
├── middlewares/
│   └── error_handler.py
├── database.py
├── app.py
└── requirements.txt
```

## Node.js/Express Target Structure

```
src/
├── config/
│   └── settings.js
├── models/
│   ├── userModel.js
│   └── courseModel.js
├── controllers/
│   ├── checkoutController.js
│   └── reportController.js
├── views/
│   └── routes.js
├── middlewares/
│   └── errorHandler.js
├── database.js
└── app.js
```

## Partially Organized Projects (e.g., task-manager-api)

When project already has `models/` and `routes/`:
1. Create `controllers/` and move business logic from routes
2. Slim routes to thin HTTP wrappers
3. Add `config/settings.py` for hardcoded values
4. Add `middlewares/error_handler.py`
5. Fix security issues in models (password hashing, response sanitization)
6. Do NOT break existing endpoint paths or response formats

## Validation Checklist

- [ ] No hardcoded secrets in source code
- [ ] All SQL uses parameterized queries
- [ ] Passwords never in API responses
- [ ] Error handling centralized
- [ ] Each file has single responsibility
- [ ] Entry point is composition root only
- [ ] All original endpoints preserved
