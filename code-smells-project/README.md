# code-smells-project

API de E-commerce em Python/Flask usada como entrada do desafio `refactor-arch`.

## Como rodar

```bash
pip install -r requirements.txt
python app.py
```

A aplicação sobe em `http://localhost:5000`. O banco SQLite (`loja.db`) é criado automaticamente no primeiro boot, já com produtos e usuários de exemplo.

## Testar endpoints

Use o arquivo [`app.http`](app.http) com a extensão **REST Client** (VS Code/Cursor) ou **HTTP Client** (JetBrains) para executar todas as requisições da API, incluindo payloads de teste para operações de escrita.

Usuários seed para login: `joao@email.com` / `123456`, `admin@loja.com` / `admin123`.
