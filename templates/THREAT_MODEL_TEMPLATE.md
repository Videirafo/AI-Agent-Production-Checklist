# Threat Model Template

## System

- Agent/workflow:
- Owner:
- Version:
- High-impact actions:

## Assets

- sensitive data:
- credentials/tokens:
- business actions:
- customer/tenant resources:

## Trust boundaries

```text
User → UI/Channel → Agent Gateway → Model → RAG/Memory → Tools → Business Systems
```

Customize the diagram above for the real system.

## Threats

| ID | Threat | Entry point | Impact | Existing controls | Residual risk | Action |
|---|---|---|---|---|---|---|
| T-001 | Prompt injection |  |  |  |  |  |
| T-002 | Excessive agency |  |  |  |  |  |
| T-003 | Sensitive disclosure |  |  |  |  |  |
| T-004 | Cross-tenant leakage |  |  |  |  |  |
| T-005 | Tool abuse |  |  |  |  |  |

## Abuse cases

Document at least:

1. malicious user;
2. malicious retrieved document;
3. compromised tool/integration;
4. user trying to cross tenant boundary;
5. accidental model hallucination causing action;
6. runaway loop/cost spike.

## Kill switches

- disable agent:
- disable tool:
- revoke credential:
- block user/tenant:
- rollback version:

## Sign-off

- [ ] threat model reviewed
- [ ] high-risk items have owner
- [ ] regression tests created for relevant threats
