# RAG, Memory & Data Isolation

## RAG pipeline

```text
ingest
→ validate source
→ normalize
→ classify sensitivity
→ attach metadata/ACL
→ chunk
→ index
→ retrieve with authorization
→ rerank
→ context policy
→ generate
→ preserve evidence
```

## Regras de ingestão

- não indexar secrets, credenciais ou dumps sem necessidade explícita;
- registrar provenance/source;
- associar tenant/owner/ACL antes do documento entrar no índice;
- versionar documentos mutáveis;
- retirar documentos deletados de todas as camadas de cache/índice.

## Retrieval seguro

O filtro de autorização deve acontecer **antes de o conteúdo chegar ao modelo**.

```text
identity + tenant + permissions
            ↓
authorized candidate set
            ↓
semantic/vector retrieval
            ↓
rerank
            ↓
model context
```

Evite recuperar globalmente e pedir ao modelo que "ignore" documentos sem permissão.

## Memória

Separar:

### Session memory

Contexto temporário da conversa/run.

### Durable memory

Fatos persistidos para reutilização futura.

Para memória persistente, definir:

- quem pode escrever;
- o que pode ser lembrado;
- provenance;
- TTL/retenção;
- correção e deleção;
- isolamento por usuário/tenant;
- critérios para não salvar informação.

## Regra de autorização

Memória e RAG podem informar o agente, mas **não concedem permissão** para uma ação.

## Testes mínimos

- usuário A não recupera conteúdo do usuário B;
- tenant A não recupera conteúdo do tenant B;
- exclusão remove conteúdo do retrieval;
- alteração de ACL tem efeito no índice;
- documento contendo prompt injection não muda policy;
- memória maliciosa não autoriza tool crítica;
- logs de retrieval não expõem conteúdo sensível desnecessariamente.