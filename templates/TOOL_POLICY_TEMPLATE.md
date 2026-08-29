# Tool Policy Template

## Tool identity

- Name:
- Owner:
- Purpose:
- Risk: low / medium / high
- Mode: read / write / destructive

## Authorization

- Required user permission:
- Required tenant scope:
- Service/account scope:
- Approval required: yes / no
- Approval conditions:

## Contract

### Input schema

```json
{}
```

### Output schema

```json
{}
```

## Controls

- Timeout:
- Max retries:
- Rate limit:
- Idempotency strategy:
- Allowed domains/resources:
- Forbidden operations:
- Sensitive fields:
- Redaction rules:

## Audit events

- call requested
- authorization decision
- approval requested/approved/rejected
- call executed
- call failed
- final outcome

## Failure behavior

Describe how the agent should react when the tool times out, returns invalid data, denies authorization, or becomes unavailable.

## Security invariant

The model chooses whether to request a tool; the backend decides whether the requested action is actually allowed.