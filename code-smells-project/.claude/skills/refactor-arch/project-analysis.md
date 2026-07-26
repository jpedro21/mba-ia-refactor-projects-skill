# Project Analysis Heuristics

## Language Detection

| Signal | Language |
|--------|----------|
| `requirements.txt`, `*.py`, `app.py` | Python |
| `package.json`, `*.js`, `node_modules/` | JavaScript/Node.js |
| `go.mod`, `*.go` | Go |
| `pom.xml`, `*.java` | Java |

## Framework Detection

### Python
- `from flask import` or `Flask(` → **Flask** (read version from `requirements.txt`)
- `from fastapi import` → **FastAPI**
- `from django` → **Django**

### Node.js
- `require('express')` or `import express` → **Express** (read version from `package.json`)
- `require('fastify')` → **Fastify**
- `require('koa')` → **Koa**

## Database Detection

| Signal | Database |
|--------|----------|
| `sqlite3`, `sqlite:///` | SQLite |
| `psycopg2`, `postgresql://` | PostgreSQL |
| `pymongo`, `mongodb://` | MongoDB |
| `SQLAlchemy`, `flask_sqlalchemy` | ORM layer (check URI for actual DB) |
| `new sqlite3.Database` | SQLite (Node.js) |

### Table Discovery
- Python raw SQL: `CREATE TABLE`, `FROM <table>`, `INSERT INTO`
- SQLAlchemy: `class X(db.Model)`, `__tablename__`
- Node.js: `CREATE TABLE` in `initDb` or migration files

## Architecture Mapping

| Pattern | Description |
|---------|-------------|
| **Monolithic flat** | All logic in 2-5 root files, no directories |
| **Partial MVC** | Has `models/`, `routes/` but business logic in routes |
| **MVC** | Clear separation: models/, controllers/, views/ |
| **God Class** | Single file >200 lines handling DB + routes + business logic |

## Domain Inference

Analyze route paths and entity names:
- `/produtos`, `/pedidos`, `/usuarios` → E-commerce API
- `/api/checkout`, `/courses`, `/enrollments` → LMS / E-learning with checkout
- `/tasks`, `/users`, `/categories`, `/reports` → Task Manager API

## File Counting

Count only source files (exclude `node_modules/`, `__pycache__/`, `.git/`, test files, config files like `.env`).
