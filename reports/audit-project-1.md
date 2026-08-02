================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python + Flask 3.1.1
Files:   13 analyzed | ~500 lines of code

## Summary
CRITICAL: 0 | HIGH: 2 | MEDIUM: 2 | LOW: 1

## Findings

### [HIGH] Insecure Password Handling (AP-06)
File: models/usuario_model.py:13-14,28-30,41-46 ; database.py:72-80
Description: Senhas gravadas em plaintext no INSERT (`create`), comparadas em plaintext no
`SELECT ... WHERE email = ? AND senha = ?` (`login`), e retornáveis via
`_row_to_dict(include_password=True)`. O seed em `database.py` também insere `admin123`,
`123456` e `senha123` como texto puro.
Impact: Se o banco for exposto (backup, dump, injeção em outro endpoint), todas as
credenciais vazam sem esforço de crack. Login comparando via SQL abre espaço a timing
attacks e impede uso de hashes por design.
Recommendation: Aplicar RP-06 — `werkzeug.security.generate_password_hash` no `create` e
no seed, `check_password_hash` no `login` (buscando só por `email` e comparando em Python).
Remover o parâmetro `include_password` e a linha `data["senha"]` do dict.

### [HIGH] Sensitive Data / Direct SQL in Health Endpoint (AP-05 + AP-11)
File: app.py:32-47
Description: `/health` executa 4 queries SQL diretas dentro do handler HTTP e devolve
contagens internas sem passar por controller/model. Não expõe secrets (o endpoint antigo
retornava `secret_key`/`db_path` — isso já foi removido), mas ainda vaza estrutura interna
e concentra lógica no `app.py`.
Impact: Lógica de negócio fora dos controllers, difícil de testar; qualquer erro de SQL
vira 500 direto do composition root.
Recommendation: Mover o health check para um controller dedicado (`HealthController`) que
consulta os models existentes (`ProdutoModel.count()`, etc.) e retorna dicts. `app.py`
apenas registra a rota.

### [MEDIUM] Broad Exception Handler Leaks Message (AP-16 residual)
File: middlewares/error_handler.py:17-20
Description: `handle_exception` faz `jsonify({"erro": str(e)})` — vaza mensagens internas
(paths, stack hints) em produção.
Impact: Information disclosure sob erros inesperados.
Recommendation: Logar `e` com stack, responder com mensagem genérica `"Erro interno do
servidor"` como já é feito no handler 500.

### [MEDIUM] Missing Input Validation on Search Filters (AP-10)
File: views/routes.py:15-19
Description: `float(request.args.get("preco_min"))` sem try/except; string inválida
retorna 500 em vez de 400.
Impact: UX ruim e ruído em logs de erro.
Recommendation: Extrair parsing para um helper em `controllers/` ou middleware de
validação; retornar 400 com mensagem clara.

### [LOW] Weak Default SECRET_KEY (AP-02 residual)
File: config/settings.py:3
Description: `SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-in-production")`
— o fallback ainda funciona silenciosamente em produção se a env var não estiver setada.
Impact: Deploy sem `SECRET_KEY` seta uma chave conhecida, permitindo forge de sessão.
Recommendation: Em produção (`DEBUG=false`), fail-fast se `SECRET_KEY` não estiver
definida.

================================
Total: 5 findings
================================

## Changelog vs previous audit (audit-project-1.md, rodada anterior)

Resolvidos desde a rodada anterior:
- AP-01 SQL Injection → parametrizado em todos os models (RP-01)
- AP-02 Hardcoded SECRET_KEY → movido para config/settings.py (RP-02, resta o fallback fraco)
- AP-03 God Class → separado em models/, controllers/, views/ (RP-03)
- AP-04 /admin/reset-db e /admin/query → removidos (RP-04)
- AP-07 Global db_connection → encapsulado em `Database` (RP-07)
- AP-09 N+1 em pedidos → JOIN em `PedidoModel.get_by_usuario/get_all` (RP-09)
- AP-14 Magic numbers de desconto → `config/settings.py` (RP-12)
- AP-13 Print → `logging` (RP em espírito)

Ainda pendente (esta é a razão principal da rodada):
- AP-06 Insecure Password Handling → NÃO foi aplicado; alvo desta Phase 3.
