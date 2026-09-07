# Safe Agent API + Playground

Projeto executável do **AI Agent Production Checklist**. Demonstra autorização determinística, aprovação humana e auditoria correlacionada para tools de agentes sem depender de LLM, API key ou banco externo.

## Usar no navegador

### GitHub Codespaces

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/Videirafo/AI-Agent-Production-Checklist?quickstart=1)

O ambiente instala as dependências, inicia a API e encaminha a porta `8000` automaticamente.

### Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FVideirafo%2FAI-Agent-Production-Checklist&root-directory=examples%2Fsafe-agent-api&project-name=safe-agent-api&repository-name=safe-agent-api)

O `pyproject.toml` declara `app.main:app` como entrypoint do FastAPI/Vercel.

## Rodar com Docker

```bash
git clone https://github.com/Videirafo/AI-Agent-Production-Checklist.git
cd AI-Agent-Production-Checklist/examples/safe-agent-api
docker compose up --build
```

Abra:

- Playground: `http://127.0.0.1:8000/`
- API docs: `http://127.0.0.1:8000/docs`
- health: `http://127.0.0.1:8000/health`

## Playground

A página `/` permite executar cinco cenários sem escrever JSON manualmente:

1. leitura permitida no mesmo tenant;
2. leitura cross-tenant negada;
3. notificação bloqueada sem aprovação humana;
4. notificação aprovada e auditada;
5. delete bloqueado pela policy da demo.

A UI chama `POST /v1/run-demo` da própria FastAPI. A policy não é reimplementada no frontend.

## O que demonstra

- tenant isolation;
- least privilege;
- approval gate humano;
- bloqueio de tool destrutiva;
- audit event estruturado;
- `request_id` propagado como `correlation_id`;
- contratos Pydantic com limites de tamanho;
- OpenAPI automática;
- headers defensivos na UI pública;
- testes de segurança com pytest;
- Docker, Codespaces e deploy Vercel-ready.

## Políticas

| Tool | Regra |
|---|---|
| `read_record` | permitida somente no mesmo tenant |
| `send_notification` | exige `human_approved=true` |
| `delete_record` | desabilitada no exemplo |

A autorização é executada **fora do prompt/modelo**. Um LLM pode sugerir uma ação, mas não concede a si mesmo permissão para executá-la.

## Audit + correlation

`POST /v1/run-demo` recebe um `request_id`. A resposta inclui um `audit_event` cujo `correlation_id` usa o mesmo identificador.

```json
{
  "request_id": "req-demo-002",
  "actor_tenant_id": "alpha",
  "resource_tenant_id": "alpha",
  "tool": "send_notification",
  "human_approved": true
}
```

A resposta registra `allowed`, `executed`, `reason`, tenants, tool e `human_approved`, sem armazenar prompt ou conteúdo de conversa.

## VS Code / Python

```bash
git clone https://github.com/Videirafo/AI-Agent-Production-Checklist.git
cd AI-Agent-Production-Checklist/examples/safe-agent-api
code .
python -m venv .venv
```

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
pytest
fastapi dev app/main.py
```

### Linux/macOS

```bash
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
fastapi dev app/main.py
```

## Fazer sua branch

```bash
git checkout -b feat/minha-policy
git add .
git commit -m "feat: add agent tool policy"
git push -u origin feat/minha-policy
```
