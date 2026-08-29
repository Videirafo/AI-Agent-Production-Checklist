# Evals & Observability

## O que medir

Um agente útil precisa ser avaliado pelo resultado da tarefa, e não apenas pela qualidade textual.

### Functional evals

- task success;
- correct tool selection;
- correct tool arguments;
- correct handoff;
- grounded answer;
- expected refusal;
- recovery after tool failure.

### Security evals

- direct prompt injection;
- indirect prompt injection;
- unauthorized tool use;
- cross-tenant retrieval;
- sensitive data disclosure;
- privilege escalation;
- dangerous retry/loop behavior.

### Operational metrics

- p50/p95 latency;
- tool error rate;
- model error rate;
- tokens/cost;
- cost per successful task;
- handoff rate;
- user correction rate;
- retry rate;
- policy-block rate.

## Regression gate

Toda mudança relevante em:

```text
model
prompt/instructions
tool schema
tool permissions
retrieval/index
memory policy
guardrails
orchestration
```

deve executar um conjunto de regressão antes de produção.

## Golden set

Um golden set deve conter casos representativos reais e versões sanitizadas de incidentes anteriores.

Cada caso pode registrar:

```yaml
id: AGENT-EVAL-001
input: "..."
expected_outcome: "..."
allowed_tools: []
forbidden_tools: []
expected_handoff: false
risk: low
```

## Tracing

Um trace útil conecta:

```text
request
→ policy decision
→ model turn
→ retrieval
→ tool call
→ approval
→ tool result
→ final output
→ outcome
```

## Dados sensíveis em traces

- não registrar secrets;
- redigir PII quando possível;
- restringir acesso aos traces;
- definir retenção;
- separar logs de debug de produção;
- evitar que tool errors incluam headers/tokens.

## Release decision

Um release não deve avançar quando:

- security eval regrediu;
- tool permission aumentou sem revisão;
- custo/latência ultrapassou orçamento sem decisão explícita;
- houve queda significativa em task success;
- traces não permitem explicar falhas críticas.