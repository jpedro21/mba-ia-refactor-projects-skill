================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python + Flask
Files:   4 analyzed | ~800 lines of code

## Summary
CRITICAL: 4 | HIGH: 3 | MEDIUM: 2 | LOW: 2

## Findings

### [CRITICAL] SQL Injection via String Concatenation
File: models.py:28-29,47-49,109-110,285-297
Description: Queries SQL construídas com concatenação de strings contendo input do usuário (id, nome, email, termo de busca).
Impact: Comprometimento total do banco de dados, roubo ou destruição de dados.
Recommendation: Usar queries parametrizadas com placeholders `?`.

### [CRITICAL] Hardcoded Credentials
File: app.py:7
Description: SECRET_KEY hardcoded como 'minha-chave-super-secreta-123'.
Impact: Exposição de credenciais no controle de versão.
Recommendation: Mover para config/settings.py com variáveis de ambiente.

### [CRITICAL] God Class / God File
File: models.py:1-314
Description: Arquivo único contém toda lógica de acesso a dados para 4 domínios (produtos, usuários, pedidos, relatórios).
Impact: Impossível testar em isolamento, qualquer mudança afeta tudo.
Recommendation: Separar em models por domínio e controllers dedicados.

### [CRITICAL] Unrestricted Admin Endpoints
File: app.py:47-78
Description: Endpoints /admin/reset-db e /admin/query permitem reset do banco e execução de SQL arbitrário sem autenticação.
Impact: Perda total de dados ou execução de comandos maliciosos.
Recommendation: Remover endpoints ou proteger com autenticação.

### [HIGH] Business Logic in Controllers
File: controllers.py:188-220,257-290
Description: Controllers contêm lógica de notificação (print), validação extensa e health check com exposição de secrets.
Impact: Lógica de negócio acoplada à camada HTTP, difícil de testar.
Recommendation: Extrair para controllers de domínio e sanitizar responses.

### [HIGH] Insecure Password Handling
File: models.py:72-87,105-120
Description: Senhas armazenadas e comparadas em plaintext; retornadas em get_todos_usuarios().
Impact: Comprometimento de contas se o banco for violado.
Recommendation: Nunca retornar senhas em responses; usar hashing seguro.

### [HIGH] Global Mutable State
File: database.py:4-9
Description: Variável global `db_connection` compartilhada entre todas as requisições.
Impact: Race conditions e vazamento de estado entre requests.
Recommendation: Encapsular em classe Database com injeção de dependência.

### [MEDIUM] N+1 Query Problem
File: models.py:171-201,203-233
Description: Loop sobre pedidos com queries individuais para itens e produtos (3 cursors aninhados).
Impact: Degradação de performance com crescimento dos dados.
Recommendation: Usar JOINs para buscar dados em batch.

### [MEDIUM] Sensitive Data Exposure in Responses
File: controllers.py:276-290
Description: Health check retorna secret_key, db_path e debug=true.
Impact: Vazamento de informações sensíveis para atacantes.
Recommendation: Sanitizar responses removendo dados internos.

### [LOW] Print-Based Logging
File: controllers.py:8,57,208-210
Description: Uso de print() para logging de eventos e erros.
Impact: Sem níveis de log, difícil monitorar em produção.
Recommendation: Usar módulo logging.

### [LOW] Magic Numbers
File: models.py:257-262
Description: Thresholds de desconto (10000, 5000, 1000) hardcoded sem constantes nomeadas.
Impact: Dificulta manutenção e consistência.
Recommendation: Extrair para config/settings.py.

================================
Total: 11 findings
================================
