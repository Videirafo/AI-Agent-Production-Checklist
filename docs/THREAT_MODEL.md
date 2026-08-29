# Threat Model for AI Agents

## Trust boundaries

Mapeie explicitamente as fronteiras:

```text
User
→ Channel/UI
→ Agent Gateway
→ Model Provider
→ Retrieval / Memory
→ Tool Registry
→ External APIs
→ Business Data
→ Human Operator
```

Tudo que atravessa uma fronteira deve ser autenticado, validado, autorizado ou tratado como não confiável conforme o caso.

## Principais ameaças

| Ameaça | Exemplo | Controles |
|---|---|---|
| Direct prompt injection | usuário tenta sobrescrever a policy | guardrails, policy externa, autorização determinística |
| Indirect prompt injection | documento/site instrui o agente a executar ação | tratar retrieval/tool output como dados, não autoridade |
| Excessive agency | agente pode deletar/enviar/pagar sem necessidade | least privilege, tool allowlist, approvals |
| Sensitive disclosure | prompt/tool/log expõe segredo ou PII | minimização, redaction, ACL, retenção |
| Cross-tenant leakage | RAG retorna conteúdo de outro cliente | tenant filter obrigatório em storage/retrieval/tool |
| Tool argument manipulation | modelo gera alvo/valor inesperado | schemas, constraints, server-side validation |
| Confused deputy | tool usa privilégio do serviço em favor de usuário não autorizado | bind identity, scope e tenant em cada chamada |
| SSRF / unsafe fetch | agente acessa host interno via URL | URL policy, allowlist/denylist, network sandbox |
| Arbitrary code execution | output vira shell/python sem controle | sandbox, approvals, resource limits |
| Cost denial | loops e tool storms | max turns, budgets, rate limit, timeout |
| Poisoned memory | input malicioso vira memória persistente | write policy, validation, provenance, deletion |
| Supply chain | tool/MCP/dependency comprometida | pinning, provenance, review, minimal permissions |

## Threat-model questions

1. Qual é a ação de maior impacto que o agente consegue executar?
2. Quais dados ele consegue ler?
3. Qual componente decide autorização?
4. Um documento recuperado consegue mudar a decisão de permissão?
5. Uma tool comprometida consegue chamar outra tool?
6. O agente pode agir fora do tenant do usuário?
7. Existe caminho para exfiltração via logs, traces ou mensagens?
8. Qual é o limite de chamadas, tempo e custo?
9. Como interromper todas as ações em segundos/minutos?
10. Como provar depois o que aconteceu?

## Security invariant

> O modelo pode sugerir uma ação; apenas uma camada confiável e determinística pode autorizá-la.