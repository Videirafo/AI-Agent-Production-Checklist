# Deploy the Safe Agent Playground on Render

This repository includes a root-level `render.yaml` Blueprint for the executable FastAPI example.

## One-click deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https%3A%2F%2Fgithub.com%2FVideirafo%2FAI-Agent-Production-Checklist)

The Blueprint creates a **Free** Python web service named `safe-agent-playground` from `examples/safe-agent-api`.

## Runtime contract

- build: `pip install -e .`
- start: `fastapi run app/main.py --host 0.0.0.0 --port $PORT`
- health check: `/health`
- no secrets required
- no database required
- no LLM/provider required
- deploy only after linked CI checks pass

## Verify after deploy

Open the generated `onrender.com` URL and verify:

1. `/` renders **Safe Agent Playground** and shows `API online`.
2. `/health` returns `status=ok` and version `0.5.0` or newer.
3. `/docs` renders the FastAPI OpenAPI UI.
4. Cross-tenant read is denied with `tenant_mismatch`.
5. Notification without approval is denied with `human_approval_required`.
6. Approved notification is allowed and emits an audit event.
7. Delete remains denied with `destructive_tool_disabled_in_demo`.

## Free-tier note

Render Free web services can spin down after a period without inbound traffic and start again on the next request. This demo is stateless, so no local state is required to survive restarts.
