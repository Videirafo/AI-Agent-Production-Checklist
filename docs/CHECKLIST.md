# Production Checklist

Use este documento antes de promover um agente para produção e novamente sempre que mudar modelo, prompt, tools, retrieval, memória, permissões ou integrações.

## 1. Escopo e governança

- [ ] problema e usuário-alvo estão definidos;
- [ ] responsabilidades do agente e do humano estão separadas;
- [ ] ações proibidas estão documentadas;
- [ ] existe owner técnico e owner de negócio;
- [ ] impacto de falha foi classificado;
- [ ] existe fallback sem IA para fluxo crítico quando necessário;
- [ ] termos, políticas e requisitos regulatórios aplicáveis foram identificados.

## 2. Identidade, sessão e tenant

- [ ] identidade é resolvida antes de qualquer ação protegida;
- [ ] `tenant_id`/ownership não vem de texto livre gerado pelo modelo;
- [ ] autorização é aplicada no backend/tool, não só no prompt;
- [ ] memória, retrieval, cache e logs respeitam isolamento;
- [ ] sessão expirada não preserva privilégios antigos;
- [ ] impersonation/admin flows são auditados separadamente.

## 3. Model e instruções

- [ ] instruções são versionadas;
- [ ] output estruturado é usado para decisões críticas;
- [ ] temperatura/controles são adequados ao fluxo;
- [ ] fallback de modelo está testado;
- [ ] mudança de modelo dispara regressão;
- [ ] instruções não contêm secrets.

## 4. Tool registry

Para cada tool registrar:

```text
name
purpose
owner
read/write/destructive
required permissions
input schema
output schema
timeout
rate limit
idempotency strategy
approval requirement
audit events
failure behavior
```

Checklist:

- [ ] tool surface mínima;
- [ ] argumentos validados server-side;
- [ ] URLs/domínios restritos quando aplicável;
- [ ] SQL/shell/código não é executado sem sandbox/controle explícito;
- [ ] escrita e exclusão têm barreiras adicionais;
- [ ] tool errors não retornam secrets ao modelo;
- [ ] retries são limitados e idempotentes.

## 5. Approval gates

Exigir aprovação humana ou política determinística para ações como:

- pagamentos e reembolsos;
- exclusão ou alteração irreversível;
- envio público de mensagens;
- mudança de permissões;
- execução de código fora de sandbox;
- acesso a dados altamente sensíveis;
- ações com custo financeiro significativo.

A tela/etapa de aprovação deve mostrar **ação, alvo, argumentos relevantes e consequência esperada**.

## 6. Prompt injection e conteúdo não confiável

- [ ] páginas web, anexos, e-mails, RAG e tool outputs são tratados como dados;
- [ ] conteúdo recuperado não concede permissão;
- [ ] instruções conflitantes vindas de dados são ignoradas pela camada de policy;
- [ ] links/URLs são validados antes de fetch/ação;
- [ ] modelos não escolhem credenciais;
- [ ] output validation ocorre antes de chamadas downstream.

## 7. RAG

- [ ] pipeline de ingestão valida origem;
- [ ] metadata inclui source, owner/tenant e versão;
- [ ] retrieval aplica ACL antes do ranking final;
- [ ] documentos excluídos saem também do índice;
- [ ] conteúdo antigo possui estratégia de atualização;
- [ ] existe limite de contexto;
- [ ] fontes aparecem no resultado quando a tarefa exige evidência.

## 8. Memória

- [ ] separar memória de sessão e memória persistente;
- [ ] definir o que pode ser lembrado;
- [ ] definir TTL/retenção;
- [ ] permitir correção/deleção quando necessário;
- [ ] secrets e credenciais não entram em memória;
- [ ] memórias recuperadas são consideradas não confiáveis para autorização.

## 9. Evals

Dataset mínimo deve incluir:

- happy paths;
- ambiguidades;
- inputs adversariais;
- prompt injection direta e indireta;
- autorização negada;
- cross-tenant attempts;
- tool argument errors;
- indisponibilidade de integração;
- loops/retries;
- handoff correto;
- recusa correta;
- regressões de incidentes anteriores.

Métricas úteis:

```text
task_success
correct_tool_rate
tool_argument_accuracy
groundedness
retrieval_precision
policy_violation_rate
handoff_precision
latency
cost_per_successful_task
user-correction-rate
```

## 10. Observabilidade

Registrar somente o necessário e com redaction quando apropriado:

- request/run/trace ID;
- workflow/agent version;
- model version;
- tool calls;
- policy/approval outcomes;
- retrieval metadata;
- token/cost/latency;
- errors;
- final outcome.

- [ ] dashboards existem para taxa de erro, latência e custo;
- [ ] alertas são acionáveis;
- [ ] traces sensíveis têm acesso restrito;
- [ ] deploy/change event aparece no timeline operacional.

## 11. Resiliência

- [ ] timeouts por tool/model;
- [ ] retry com backoff e limite;
- [ ] circuit breaker quando aplicável;
- [ ] idempotency key para ações repetíveis de risco;
- [ ] filas possuem DLQ/recovery quando necessário;
- [ ] agente possui max turns/max tools/max cost;
- [ ] existe kill switch.

## 12. Deploy

```text
EVALS GREEN
→ SECURITY CHECK
→ STAGING
→ CANARY / LIMITED AUDIENCE
→ METRICS & TRACES
→ EXPAND
→ OBSERVE
```

- [ ] configuração é versionada;
- [ ] rollback de prompt/model/tool está definido;
- [ ] migration de memória/index possui plano de retorno;
- [ ] smoke tests cobrem tools críticas;
- [ ] mudanças relevantes aparecem no changelog.

## 13. Incident response

O runbook deve responder:

1. como desabilitar uma tool;
2. como bloquear um tenant/user abusivo;
3. como revogar credenciais;
4. como parar o agente;
5. como preservar evidência sem expor PII;
6. como identificar runs afetadas;
7. como corrigir e adicionar teste de regressão.

## Definition of Production Ready

Um agente só é production-ready quando **seu comportamento crítico pode ser observado, testado, limitado e interrompido**.