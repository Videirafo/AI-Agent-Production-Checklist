# Engineering Workflow — AI Agent Production

Este repositório combina **Programação Vibe + Videira Master Context** com os controles específicos de agentes de IA.

## Fluxo
Ideia → pesquisa → usuário → PRD → arquitetura do agente → política de ferramentas → tarefas → implementação → testes/evals → segurança → review → canário/QA → produção → observabilidade → iteração.

## Por mudança
**Ler → Compreender → Planejar → Implementar → Testar/Evaluar → Revisar → Corrigir → Commit → Atualizar documentação.**

## Requisitos adicionais para agentes
- Contrato claro de entrada/saída.
- Ferramentas com allowlist, escopo e autorização.
- Aprovação humana para ações de risco quando aplicável.
- Fail-closed quando identidade, permissão ou contexto forem insuficientes.
- Não inventar sucesso de ferramentas.
- Idempotência para mutações.
- Audit trail e recibo de execução.
- Evals de sucesso, recusa, erro, timeout, prompt injection e cross-tenant.
- Segredos nunca entram em prompt/log público.
- Métricas de qualidade, custo, latência e falha.

## Gate
Testes + evals + segurança + revisão de políticas → preview/canário → produção → monitoramento → rollback.
