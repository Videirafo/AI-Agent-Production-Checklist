# Safe Agent API

Projeto executável do **AI Agent Production Checklist**. Demonstra uma camada determinística de autorização, aprovação e auditoria para tools de agentes sem depender de LLM ou API key.

## O que demonstra

- tenant isolation;
- least privilege;
- approval gate humano;
- bloqueio de tool destrutiva;
- audit event estruturado;
- `request_id` propagado como `correlation_id`;
- contratos Pydantic;
- API FastAPI com OpenAPI automática;
- testes de segurança com pytest;
- execução via Docker.

## Rodar com Docker

```bash
git clone https://github.com/Videirafo/AI-Agent-Production-Checklist.git
cd AI-Agent-Production-Checklist/examples/safe-agent-api
docker compose up --build
```

Abra:

- API docs: `http://127.0.0.1:8000/docs`
- health: `http://127.0.0.1:8000/health`

## Clonar e abrir no VS Code

```bash
git clone https://github.com/Videirafo/AI-Agent-Production-Checklist.git
cd AI-Agent-Production-Checklist/examples/safe-agent-api
code .
```

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
fastapi dev app/main.py
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
fastapi dev app/main.py
```

## Executar testes

```bash
pytest
```

## Políticas

| Tool | Regra |
|---|---|
| `read_record` | permitida somente no mesmo tenant |
| `send_notification` | exige `human_approved=true` |
| `delete_record` | desabilitada no exemplo |

A autorização é executada **fora do prompt/modelo**. Um LLM pode sugerir uma ação, mas não concede a si mesmo permissão para executá-la.

## Audit + correlation

`POST /v1/run-demo` recebe um `request_id`. A resposta inclui um `audit_event` cujo `correlation_id` usa o mesmo identificador. Assim uma decisão permitida ou negada pode ser ligada à execução e ao diagnóstico operacional.

Exemplo:

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

## Fazer sua branch

```bash
git checkout -b feat/minha-policy
git add .
git commit -m "feat: add agent tool policy"
git push -u origin feat/minha-policy
```
