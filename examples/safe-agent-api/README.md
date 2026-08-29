# Safe Agent API

Projeto executável do **AI Agent Production Checklist**. Ele demonstra uma camada determinística de autorização para tools de agentes sem depender de LLM ou API key.

## O que demonstra

- tenant isolation;
- least privilege;
- approval gate humano;
- bloqueio de tool destrutiva;
- contratos Pydantic;
- API FastAPI com OpenAPI automática;
- testes de segurança com pytest.

## Clonar e abrir no VS Code

```bash
git clone https://github.com/Videirafo/AI-Agent-Production-Checklist.git
cd AI-Agent-Production-Checklist/examples/safe-agent-api
code .
```

Crie o ambiente e instale:

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
fastapi dev
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
fastapi dev
```

Abra:

- API docs: `http://127.0.0.1:8000/docs`
- health: `http://127.0.0.1:8000/health`

## Executar testes

```bash
pytest
```

## Exemplo de política

| Tool | Regra |
|---|---|
| `read_record` | permitida somente no mesmo tenant |
| `send_notification` | exige `human_approved=true` |
| `delete_record` | desabilitada no exemplo |

A autorização é executada **fora do prompt/modelo**. Um LLM pode sugerir uma ação, mas não concede a si mesmo permissão para executá-la.

## Teste manual

POST `/v1/tool-check`:

```json
{
  "actor_tenant_id": "alpha",
  "resource_tenant_id": "alpha",
  "tool": "send_notification",
  "human_approved": false
}
```

O resultado deve indicar `human_approval_required`.

## Fazer sua branch

```bash
git checkout -b feat/minha-policy
git add .
git commit -m "feat: add agent tool policy"
git push -u origin feat/minha-policy
```
