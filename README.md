# Criação de Skills — Refatoração Arquitetural Automatizada

## Análise Manual

### Projeto 1 — code-smells-project (Python/Flask — E-commerce)

| # | Severidade | Problema | Arquivo | Justificativa |
|---|-----------|----------|---------|---------------|
| 1 | CRITICAL | SQL Injection via concatenação de strings | `models.py:28-297` | Queries com input do usuário permitem execução arbitrária de SQL |
| 2 | CRITICAL | SECRET_KEY hardcoded | `app.py:7` | Credencial exposta no código-fonte e versionamento |
| 3 | CRITICAL | God File com toda lógica de dados | `models.py:1-314` | 4 domínios em um arquivo, impossível testar isoladamente |
| 4 | CRITICAL | Endpoints admin sem autenticação | `app.py:47-78` | `/admin/query` executa SQL arbitrário |
| 5 | HIGH | Senhas em plaintext nas responses | `models.py:72-87` | `get_todos_usuarios()` retorna campo `senha` |
| 6 | MEDIUM | N+1 queries em pedidos | `models.py:171-233` | 3 cursors aninhados por pedido |
| 7 | MEDIUM | Health check expõe secrets | `controllers.py:276-290` | Retorna `secret_key`, `db_path`, `debug` |
| 8 | LOW | Magic numbers em descontos | `models.py:257-262` | Thresholds 10000/5000/1000 sem constantes |
| 9 | LOW | Print-based logging | `controllers.py:8-210` | Sem níveis de log estruturados |

### Projeto 2 — ecommerce-api-legacy (Node.js/Express — LMS)

| # | Severidade | Problema | Arquivo | Justificativa |
|---|-----------|----------|---------|---------------|
| 1 | CRITICAL | God Class AppManager | `AppManager.js:1-141` | DB + rotas + checkout em uma classe |
| 2 | CRITICAL | Credenciais hardcoded | `utils.js:2-6` | `paymentGatewayKey`, `dbPass` no código |
| 3 | HIGH | Callback hell (4+ níveis) | `AppManager.js:80-128` | Relatório financeiro ilegível e propenso a race conditions |
| 4 | HIGH | Hash de senha inseguro (badCrypto) | `utils.js:17-23` | Função trivial facilmente reversível |
| 5 | HIGH | Lógica de checkout nas rotas | `AppManager.js:28-78` | 50 linhas de negócio inline no handler HTTP |
| 6 | MEDIUM | N+1 queries no relatório | `AppManager.js:89-125` | Loop com queries individuais por enrollment |
| 7 | MEDIUM | Cartão logado no console | `AppManager.js:45` | Violação de dados sensíveis PCI |
| 8 | LOW | Nomes de variáveis crípticos | `AppManager.js:29-33` | `u`, `e`, `p`, `cc` reduzem legibilidade |
| 9 | LOW | Delete sem cascade | `AppManager.js:131-137` | Dados órfãos no banco |

### Projeto 3 — task-manager-api (Python/Flask — Task Manager)

| # | Severidade | Problema | Arquivo | Justificativa |
|---|-----------|----------|---------|---------------|
| 1 | CRITICAL | MD5 para senhas | `models/user.py:27-32` | Algoritmo criptograficamente quebrado |
| 2 | CRITICAL | SECRET_KEY hardcoded | `app.py:13` | Credencial no código-fonte |
| 3 | HIGH | Lógica de negócio nas rotas | `routes/task_routes.py:11-299` | 300 linhas de validação e regras nos handlers |
| 4 | HIGH | Password exposto em to_dict() | `models/user.py:16-25` | Hash retornado na API |
| 5 | HIGH | N+1 queries em listagem | `routes/task_routes.py:41-57` | Query por user/category em cada task |
| 6 | MEDIUM | datetime.utcnow() deprecated | `models/task.py:15-16` | API obsoleta no Python 3.12+ |
| 7 | MEDIUM | Categorias em report_routes | `routes/report_routes.py:157-223` | Violação de SRP |
| 8 | LOW | Bare except | `routes/task_routes.py:62` | Exceções silenciadas |
| 9 | LOW | Lógica overdue duplicada | 3+ arquivos | Mesma regra copiada em vários locais |

---

## Construção da Skill

### Decisões de Design

A skill foi estruturada em **SKILL.md** (orquestrador das 3 fases) + **5 arquivos de referência** com progressive disclosure:

| Arquivo | Área de Conhecimento |
|---------|---------------------|
| `project-analysis.md` | Heurísticas de detecção de stack |
| `anti-patterns-catalog.md` | 16 anti-patterns com sinais de detecção |
| `audit-report-template.md` | Formato padronizado do relatório |
| `mvc-guidelines.md` | Regras do padrão MVC alvo |
| `refactoring-playbook.md` | 12 padrões de transformação com before/after |

### Anti-patterns Incluídos

Incluí 16 anti-patterns (mínimo 8) cobrindo todas as severidades, com foco nos problemas encontrados nos 3 projetos: SQL Injection, God Class, hardcoded credentials, callback hell, N+1, deprecated APIs, etc.

### Agnosticismo de Tecnologia

- Heurísticas separadas para Python/Flask e Node.js/Express em `project-analysis.md`
- Playbook com exemplos em ambas as linguagens
- MVC guidelines com estruturas-alvo para cada stack
- Fase 3 adapta-se ao contexto: monolito flat recebe estrutura completa; projeto parcialmente organizado recebe controllers + config sem quebrar blueprints existentes

### Desafios Encontrados

1. **Projeto parcialmente organizado (task-manager-api):** A refatoração precisou preservar blueprints e endpoints existentes, adicionando camada de controllers sem mover rotas.
2. **Callback hell no Node.js:** Promisificação das funções sqlite3 foi necessária para substituir callbacks por async/await.
3. **Compatibilidade de responses:** Endpoints originais precisaram manter formato de resposta idêntico após refatoração.

---

## Resultados

### Resumo dos Relatórios

| Projeto | CRITICAL | HIGH | MEDIUM | LOW | Total |
|---------|----------|------|--------|-----|-------|
| code-smells-project | 4 | 3 | 2 | 2 | 11 |
| ecommerce-api-legacy | 2 | 4 | 2 | 2 | 10 |
| task-manager-api | 2 | 3 | 3 | 3 | 11 |

### Comparação Antes/Depois

**code-smells-project:**
```
ANTES: app.py, controllers.py, models.py, database.py (flat)
DEPOIS: config/, models/, controllers/, views/, middlewares/, app.py
```

**ecommerce-api-legacy:**
```
ANTES: app.js, AppManager.js (God Class), utils.js
DEPOIS: config/, models/, controllers/, views/, middlewares/, database.js, app.js
```

**task-manager-api:**
```
ANTES: models/, routes/ (lógica nas rotas), services/, utils/
DEPOIS: + config/, controllers/, middlewares/ (rotas slim, lógica nos controllers)
```

### Checklist de Validação

#### Projeto 1 — code-smells-project
- [x] Fase 1: Python/Flask detectado, domínio E-commerce
- [x] Fase 2: 11 findings (4 CRITICAL)
- [x] Fase 3: MVC aplicado, app inicia, endpoints respondem

#### Projeto 2 — ecommerce-api-legacy
- [x] Fase 1: Node.js/Express detectado, domínio LMS
- [x] Fase 2: 10 findings (2 CRITICAL)
- [x] Fase 3: MVC aplicado, checkout e relatório funcionam

#### Projeto 3 — task-manager-api
- [x] Fase 1: Python/Flask detectado, domínio Task Manager
- [x] Fase 2: 11 findings (2 CRITICAL)
- [x] Fase 3: Controllers adicionados, endpoints preservados

### Logs de Validação

```
# code-smells-project
Boot OK
GET /health → {"status":"ok","database":"connected","counts":{"produtos":10,"usuarios":3,"pedidos":0}}
GET /produtos → 200 OK

# ecommerce-api-legacy
POST /api/checkout → {"msg":"Sucesso","enrollment_id":2}
GET /api/admin/financial-report → 200 OK

# task-manager-api
Boot OK
GET /health → {"status":"ok","timestamp":"2026-07-26T16:45:23+00:00"}
GET /tasks → 200 OK
```

---

## Como Executar

### Pré-requisitos

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) instalado e configurado
- Python 3.10+ com pip
- Node.js 18+ com npm

### Executar a Skill

```bash
# Projeto 1
cd code-smells-project
claude "/refactor-arch"

# Projeto 2
cd ../ecommerce-api-legacy
claude "/refactor-arch"

# Projeto 3
cd ../task-manager-api
claude "/refactor-arch"
```

A Fase 2 pausa e pede confirmação antes da refatoração. Relatórios salvos em `reports/audit-project-{1,2,3}.md`.

### Validar Refatoração

```bash
# Python/Flask
cd code-smells-project  # ou task-manager-api
pip install -r requirements.txt
python app.py
curl http://localhost:5000/health
curl http://localhost:5000/produtos  # code-smells
curl http://localhost:5000/tasks      # task-manager

# Node.js/Express
cd ecommerce-api-legacy
npm install
node src/app.js
curl -X POST http://localhost:3000/api/checkout \
  -H "Content-Type: application/json" \
  -d '{"usr":"Test","eml":"test@test.com","pwd":"123","c_id":2,"card":"4111222233334444"}'
```