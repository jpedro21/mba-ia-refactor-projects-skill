# task-manager-api

API de Task Manager em Python/Flask usada como entrada do desafio `refactor-arch`. Diferente dos outros projetos, este já possui alguma separação de camadas (`models/`, `routes/`, `services/`, `utils/`), mas ainda contém problemas arquiteturais e de qualidade.

## Como rodar

```bash
pip install -r requirements.txt
python seed.py
python app.py
```

A aplicação sobe em `http://localhost:5000`. O `seed.py` popula o banco SQLite (`tasks.db`) com usuários, categorias e tasks de exemplo — **rode-o antes do primeiro boot**, caso contrário os endpoints vão retornar listas vazias.

## Testar endpoints

Use o arquivo [`app.http`](app.http) com a extensão **REST Client** (VS Code/Cursor) ou **HTTP Client** (JetBrains) para executar todas as requisições da API, incluindo payloads de teste para operações de escrita.

Após o seed, os IDs de referência são documentados no topo do `app.http` (usuários 1–3, categorias 1–4, tasks 1–10). Login seed: `joao@email.com` / `1234`.
