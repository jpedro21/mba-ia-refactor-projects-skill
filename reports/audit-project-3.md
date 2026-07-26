================================
ARCHITECTURE AUDIT REPORT
================================
Project: task-manager-api
Stack:   Python + Flask
Files:   12 analyzed | ~1200 lines of code

## Summary
CRITICAL: 2 | HIGH: 3 | MEDIUM: 3 | LOW: 3

## Findings

### [CRITICAL] Insecure Password Handling
File: models/user.py:27-32
Description: Senhas hasheadas com MD5 (hashlib.md5), algoritmo criptograficamente quebrado.
Impact: Senhas facilmente quebráveis por rainbow tables ou força bruta.
Recommendation: Usar werkzeug.security generate_password_hash/check_password_hash.

### [CRITICAL] Hardcoded Credentials
File: app.py:13
Description: SECRET_KEY hardcoded como 'super-secret-key-123'.
Impact: Exposição de chave secreta no repositório.
Recommendation: Mover para config/settings.py com variável de ambiente.

### [HIGH] Business Logic in Routes
File: routes/task_routes.py:11-299
Description: Rotas contêm validação extensa, cálculo de overdue e lógica de negócio diretamente nos handlers.
Impact: Lógica duplicada e acoplada ao HTTP, difícil de testar.
Recommendation: Extrair para controllers/task_controller.py.

### [HIGH] Sensitive Data Exposure
File: models/user.py:16-25
Description: Método to_dict() retorna campo password (hash) na resposta da API.
Impact: Hash de senha exposto permite ataques offline.
Recommendation: Remover password de to_dict().

### [HIGH] N+1 Query Problem
File: routes/task_routes.py:41-57
Description: Loop sobre tasks com User.query.get() e Category.query.get() para cada item.
Impact: Performance degrada com volume de tasks.
Recommendation: Usar eager loading (joinedload) ou batch queries.

### [MEDIUM] Missing Controller Layer
File: routes/report_routes.py:157-223
Description: Endpoints de categorias misturados em report_routes sem camada de controller dedicada.
Impact: Responsabilidades misturadas, violação de SRP.
Recommendation: Criar CategoryController separado.

### [MEDIUM] Deprecated API Usage
File: models/task.py:15-16, routes/task_routes.py:31
Description: Uso de datetime.utcnow() deprecated no Python 3.12+.
Impact: Quebra em futuras versões do Python.
Recommendation: Usar datetime.now(timezone.utc).

### [MEDIUM] Hardcoded SMTP Credentials
File: services/notification_service.py:9-10
Description: Credenciais de email hardcoded (email_user, email_password).
Impact: Exposição de credenciais se o serviço for ativado.
Recommendation: Mover para config com variáveis de ambiente.

### [LOW] Bare Exception Handling
File: routes/task_routes.py:62-63, routes/user_routes.py:130-132
Description: except: sem tipo captura todas as exceções silenciosamente.
Impact: Bugs ocultos, debugging difícil.
Recommendation: Capturar exceções específicas e usar logging.

### [LOW] Code Duplication
File: routes/task_routes.py:30-39, routes/user_routes.py:171-180
Description: Lógica de cálculo de overdue duplicada em 3+ locais.
Impact: Inconsistências ao modificar regra de negócio.
Recommendation: Centralizar em método Task.is_overdue() ou helper.

### [LOW] Print-Based Logging
File: routes/task_routes.py:149, routes/user_routes.py:83
Description: print() para logging de eventos em vez de módulo logging.
Impact: Sem níveis de log em produção.
Recommendation: Usar logging.info().

================================
Total: 11 findings
================================
