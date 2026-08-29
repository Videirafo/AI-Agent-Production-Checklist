# AI Agent Production Readiness

## Context

- Agent/workflow:
- Owner:
- Version/commit:
- Risk level: low / medium / high
- Intended users:
- Production date:

## Scope

- [ ] purpose documented
- [ ] prohibited actions documented
- [ ] human owner defined
- [ ] fallback defined

## Identity & permissions

- [ ] authn validated
- [ ] authz enforced outside model
- [ ] tenant isolation tested
- [ ] least privilege applied
- [ ] destructive tools protected

## Tools

- [ ] schemas validated
- [ ] timeouts/retries limited
- [ ] idempotency considered
- [ ] approvals configured
- [ ] audit events emitted

## Data

- [ ] data classification complete
- [ ] RAG ACL tested
- [ ] memory policy defined
- [ ] retention/deletion defined
- [ ] logs/traces reviewed for sensitive data

## Safety & security

- [ ] prompt injection evals green
- [ ] unauthorized-action evals green
- [ ] cross-tenant evals green
- [ ] sensitive-disclosure evals green
- [ ] excessive-agency controls reviewed

## Evals

- [ ] golden set versioned
- [ ] task success acceptable
- [ ] tool accuracy acceptable
- [ ] regression suite green

## Operations

- [ ] dashboards available
- [ ] alerts configured
- [ ] cost budget defined
- [ ] kill switch tested
- [ ] rollback tested
- [ ] incident owner known

## Decision

- [ ] APPROVED FOR PRODUCTION
- [ ] BLOCKED

Reason / evidence:
