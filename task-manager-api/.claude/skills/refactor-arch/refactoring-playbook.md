# Refactoring Playbook

8+ transformation patterns with before/after examples.

---

## RP-01: Extract SQL Injection to Parameterized Queries

**Anti-pattern:** AP-01 SQL Injection

**Before (Python):**
```python
cursor.execute("SELECT * FROM produtos WHERE id = " + str(id))
cursor.execute(
    "INSERT INTO produtos (nome, preco) VALUES ('" + nome + "', " + str(preco) + ")"
)
```

**After (Python):**
```python
cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))
cursor.execute(
    "INSERT INTO produtos (nome, preco) VALUES (?, ?)",
    (nome, preco)
)
```

**Before (Node.js):**
```javascript
db.run("DELETE FROM users WHERE id = " + id);
```

**After (Node.js):**
```javascript
db.run("DELETE FROM users WHERE id = ?", [id]);
```

---

## RP-02: Extract Hardcoded Secrets to Config Module

**Anti-pattern:** AP-02 Hardcoded Credentials

**Before:**
```python
app.config["SECRET_KEY"] = "minha-chave-super-secreta-123"
```

**After:**
```python
# config/settings.py
import os
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-in-production")
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

# app.py
from config.settings import SECRET_KEY, DEBUG
app.config["SECRET_KEY"] = SECRET_KEY
```

**Before (Node.js):**
```javascript
const config = {
    paymentGatewayKey: "pk_live_1234567890abcdef",
    dbPass: "senha_super_secreta_prod_123"
};
```

**After (Node.js):**
```javascript
// config/settings.js
require('dotenv').config();
module.exports = {
    paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY,
    port: process.env.PORT || 3000
};
```

---

## RP-03: Split God Class into MVC Layers

**Anti-pattern:** AP-03 God Class

**Before:** Single `models.py` with 300+ lines of SQL + business logic + formatting.

**After:**
```
models/produto_model.py    → get_all(), get_by_id(), create(), update(), delete()
controllers/produto_controller.py → validate, orchestrate, call model
views/routes.py            → @app.route → controller.listar()
```

**Before (Node.js):**
```javascript
class AppManager {
    initDb() { /* schema + seed */ }
    setupRoutes(app) { /* all routes inline */ }
}
```

**After:**
```javascript
// database.js → initDb()
// models/courseModel.js → findById(), create()
// controllers/checkoutController.js → processCheckout()
// views/routes.js → app.post('/api/checkout', checkoutController.process)
```

---

## RP-04: Remove Dangerous Admin Endpoints

**Anti-pattern:** AP-04 Unrestricted Admin Endpoints

**Before:**
```python
@app.route("/admin/query", methods=["POST"])
def executar_query():
    query = request.get_json().get("sql", "")
    cursor.execute(query)  # arbitrary SQL execution!
```

**After:** Remove entirely, or replace with authenticated admin API using predefined safe operations.

---

## RP-05: Extract Business Logic from Routes to Controllers

**Anti-pattern:** AP-05 Business Logic in Routes

**Before:**
```python
@task_bp.route('/tasks', methods=['POST'])
def create_task():
    # 50 lines of validation, business rules, DB operations
    if len(title) < 3: ...
    task = Task()
    task.title = title
    db.session.add(task)
    db.session.commit()
```

**After:**
```python
# controllers/task_controller.py
class TaskController:
    def create(self, data):
        self._validate(data)
        return self.task_model.create(data)

# views/routes.py (thin)
@task_bp.route('/tasks', methods=['POST'])
def create_task():
    result, error = task_controller.create(request.get_json())
    if error: return jsonify({'error': error}), 400
    return jsonify(result), 201
```

---

## RP-06: Secure Password Handling

**Anti-pattern:** AP-06 Insecure Password Handling

**Before:**
```python
def set_password(self, pwd):
    self.password = hashlib.md5(pwd.encode()).hexdigest()

def to_dict(self):
    return {'password': self.password, ...}
```

**After:**
```python
from werkzeug.security import generate_password_hash, check_password_hash

def set_password(self, pwd):
    self.password = generate_password_hash(pwd)

def check_password(self, pwd):
    return check_password_hash(self.password, pwd)

def to_dict(self):
    return {'id': self.id, 'name': self.name, 'email': self.email}
    # password NEVER included
```

---

## RP-07: Replace Global State with Dependency Injection

**Anti-pattern:** AP-07 Global Mutable State

**Before:**
```python
db_connection = None
def get_db():
    global db_connection
    if db_connection is None:
        db_connection = sqlite3.connect(...)
```

**After:**
```python
class Database:
    def __init__(self, path):
        self._connection = None
        self._path = path
    def get_connection(self):
        if self._connection is None:
            self._connection = sqlite3.connect(self._path)
        return self._connection

# In app.py
db = Database(settings.DATABASE_PATH)
```

---

## RP-08: Flatten Callback Hell with Async/Await

**Anti-pattern:** AP-08 Callback Hell

**Before:**
```javascript
db.all("SELECT * FROM courses", [], (err, courses) => {
    courses.forEach(c => {
        db.all("SELECT * FROM enrollments WHERE course_id = ?", [c.id], (err, enrollments) => {
            enrollments.forEach(enr => {
                db.get("SELECT name FROM users WHERE id = ?", [enr.user_id], (err, user) => {
                    // 4 levels deep...
                });
            });
        });
    });
});
```

**After:**
```javascript
async function getFinancialReport(db) {
    const courses = await dbAll(db, "SELECT * FROM courses");
    const report = [];
    for (const course of courses) {
        const enrollments = await dbAll(db, "SELECT * FROM enrollments WHERE course_id = ?", [course.id]);
        const students = [];
        for (const enr of enrollments) {
            const user = await dbGet(db, "SELECT name FROM users WHERE id = ?", [enr.user_id]);
            const payment = await dbGet(db, "SELECT amount, status FROM payments WHERE enrollment_id = ?", [enr.id]);
            students.push({ student: user?.name || 'Unknown', paid: payment?.amount || 0 });
        }
        report.push({ course: course.title, students });
    }
    return report;
}
```

---

## RP-09: Fix N+1 Queries with JOINs

**Anti-pattern:** AP-09 N+1 Query Problem

**Before:**
```python
for row in rows:
    cursor2.execute("SELECT * FROM itens_pedido WHERE pedido_id = " + str(row["id"]))
    for item in itens:
        cursor3.execute("SELECT nome FROM produtos WHERE id = " + str(item["produto_id"]))
```

**After:**
```python
cursor.execute("""
    SELECT p.*, ip.produto_id, ip.quantidade, ip.preco_unitario, pr.nome as produto_nome
    FROM pedidos p
    LEFT JOIN itens_pedido ip ON ip.pedido_id = p.id
    LEFT JOIN produtos pr ON pr.id = ip.produto_id
    WHERE p.usuario_id = ?
""", (usuario_id,))
# Group results in Python by pedido_id
```

---

## RP-10: Centralize Error Handling

**Anti-pattern:** AP-16 Bare Exception Handling

**Before:** Every route has its own try/except returning 500.

**After (Python/Flask):**
```python
# middlewares/error_handler.py
def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(str(e))
        return jsonify({'error': 'Erro interno do servidor'}), 500

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Recurso não encontrado'}), 404
```

**After (Node.js/Express):**
```javascript
// middlewares/errorHandler.js
function errorHandler(err, req, res, next) {
    console.error(err.stack);
    res.status(err.status || 500).json({ error: err.message || 'Internal Server Error' });
}
module.exports = errorHandler;
```

---

## RP-11: Replace Deprecated APIs

**Anti-pattern:** AP-12 Deprecated API Usage

**Before:**
```python
from datetime import datetime
task.created_at = datetime.utcnow()
```

**After:**
```python
from datetime import datetime, timezone
task.created_at = datetime.now(timezone.utc)
```

---

## RP-12: Extract Magic Numbers to Constants

**Anti-pattern:** AP-14 Magic Numbers

**Before:**
```python
if faturamento > 10000:
    desconto = faturamento * 0.1
elif faturamento > 5000:
    desconto = faturamento * 0.05
```

**After:**
```python
# config/settings.py
DISCOUNT_TIER_HIGH = 10000
DISCOUNT_TIER_MEDIUM = 5000
DISCOUNT_RATE_HIGH = 0.10
DISCOUNT_RATE_MEDIUM = 0.05
```
