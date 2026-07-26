# ecommerce-api-legacy

LMS API (com fluxo de checkout) em Node.js/Express usada como entrada do desafio `refactor-arch`.

## Como rodar

```bash
npm install
npm start
```

A aplicação sobe em `http://localhost:3000`. O banco SQLite é em memória e já carrega seeds automaticamente no boot.

## Testar endpoints

Use o arquivo [`app.http`](app.http) com a extensão **REST Client** (VS Code/Cursor) ou **HTTP Client** (JetBrains) para executar todas as requisições da API, incluindo payloads de teste para checkout, relatório financeiro e exclusão de usuários.

Cursos seed: `1` = Clean Architecture, `2` = Docker. Cartões que começam com `4` são aprovados.
