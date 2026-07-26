================================
ARCHITECTURE AUDIT REPORT
================================
Project: ecommerce-api-legacy
Stack:   JavaScript + Express
Files:   3 analyzed | ~170 lines of code

## Summary
CRITICAL: 2 | HIGH: 4 | MEDIUM: 2 | LOW: 2

## Findings

### [CRITICAL] God Class / God File
File: AppManager.js:1-141
Description: Classe AppManager contém inicialização do banco, seed de dados, definição de todas as rotas e lógica de checkout/pagamento.
Impact: Violação total da separação de responsabilidades, impossível testar em isolamento.
Recommendation: Dividir em models/, controllers/, views/ e database.js.

### [CRITICAL] Hardcoded Credentials
File: utils.js:2-6
Description: Credenciais hardcoded: dbPass, paymentGatewayKey, smtpUser expostas no código-fonte.
Impact: Exposição de chaves de produção no repositório.
Recommendation: Mover para config/settings.js com variáveis de ambiente.

### [HIGH] Callback Hell / Deep Nesting
File: AppManager.js:80-128
Description: Relatório financeiro com 4+ níveis de callbacks aninhados (db.all → forEach → db.all → forEach → db.get).
Impact: Código ilegível, propenso a erros de race condition na montagem do relatório.
Recommendation: Usar async/await com funções auxiliares promisificadas.

### [HIGH] Insecure Password Handling
File: utils.js:17-23, AppManager.js:68
Description: Função badCrypto() com hash trivial; senhas armazenadas com hash inseguro.
Impact: Senhas facilmente reversíveis ou colidíveis.
Recommendation: Usar crypto.createHash('sha256') ou bcrypt.

### [HIGH] Business Logic in Routes
File: AppManager.js:28-78
Description: Lógica completa de checkout (validação, pagamento, matrícula, auditoria) inline na definição da rota.
Impact: Impossível reutilizar ou testar lógica de negócio separadamente.
Recommendation: Extrair para checkoutController.js.

### [HIGH] Global Mutable State
File: utils.js:9-10
Description: globalCache e totalRevenue como variáveis globais mutáveis compartilhadas entre requests.
Impact: Vazamento de dados entre requisições concorrentes.
Recommendation: Remover estado global ou usar cache request-scoped.

### [MEDIUM] N+1 Query Problem
File: AppManager.js:89-125
Description: Loop sobre courses com queries individuais para enrollments, users e payments.
Impact: Performance degrada linearmente com volume de dados.
Recommendation: Usar JOINs ou queries em batch com async/await.

### [MEDIUM] Sensitive Data Exposure
File: AppManager.js:45
Description: Número do cartão de crédito e chave do gateway logados no console.
Impact: Violação PCI-DSS, exposição de dados financeiros.
Recommendation: Nunca logar dados de cartão; mascarar informações sensíveis.

### [LOW] Poor Variable Naming
File: AppManager.js:29-33
Description: Variáveis de request com nomes crípticos: u, e, p, cid, cc e campos usr, eml, pwd.
Impact: Reduz legibilidade e dificulta manutenção.
Recommendation: Usar nomes descritivos (name, email, password, courseId, cardNumber).

### [LOW] Missing Error Handling
File: AppManager.js:131-137
Description: DELETE /api/users/:id não trata erros do banco e não limpa dados relacionados.
Impact: Dados órfãos (enrollments, payments) permanecem no banco.
Recommendation: Implementar cascade delete e tratamento de erros.

================================
Total: 10 findings
================================
