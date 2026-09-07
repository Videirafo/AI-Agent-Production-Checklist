PUBLIC_URL = "https://safe-agent-playground.onrender.com"
SOURCE_URL = "https://github.com/Videirafo/AI-Agent-Production-Checklist"

LLMS_TXT = f"""# Safe Agent Playground

> Runnable open-source FastAPI demo for AI-agent tool authorization boundaries. The model may suggest an action; deterministic policy and human approval decide whether execution is allowed.

## Primary resources
- [Live Playground]({PUBLIC_URL}/): interactive policy, approval, execution and audit demo
- [OpenAPI]({PUBLIC_URL}/openapi.json): machine-readable API schema
- [Swagger UI]({PUBLIC_URL}/docs): interactive API documentation
- [Playground Markdown]({PUBLIC_URL}/playground.md): text-first description of the demo
- [Source]({SOURCE_URL}): MIT-licensed source code and contribution workflow

## Safety model
- tenant isolation
- deterministic tool policy
- human approval for sensitive actions
- destructive-action blocking
- structured audit events
- correlation IDs

## Optional
- [Health]({PUBLIC_URL}/health)
- [AGENTS.md]({PUBLIC_URL}/AGENTS.md)
- [Sitemap]({PUBLIC_URL}/sitemap.md)
"""

LLMS_FULL_TXT = LLMS_TXT + """

## Demo scenarios
1. same-tenant read -> allowed and executed
2. cross-tenant read -> denied with tenant_mismatch
3. notification without approval -> denied with human_approval_required
4. approved notification -> allowed, executed and audited
5. delete_record -> blocked with destructive_tool_disabled_in_demo

## Execution flow
model suggestion -> deterministic policy -> human approval -> execution -> structured audit event -> correlation ID

No LLM, API key, signup, external database or provider is required by the demo.
"""

ROBOTS_TXT = f"""User-agent: *
Allow: /

Sitemap: {PUBLIC_URL}/sitemap.xml
"""

SITEMAP_XML = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{PUBLIC_URL}/</loc></url>
  <url><loc>{PUBLIC_URL}/docs</loc></url>
  <url><loc>{PUBLIC_URL}/openapi.json</loc></url>
  <url><loc>{PUBLIC_URL}/playground.md</loc></url>
  <url><loc>{PUBLIC_URL}/llms.txt</loc></url>
  <url><loc>{PUBLIC_URL}/AGENTS.md</loc></url>
</urlset>
"""

SITEMAP_MD = f"""# Safe Agent Playground Sitemap

- [Playground]({PUBLIC_URL}/)
- [OpenAPI / Swagger]({PUBLIC_URL}/docs)
- [OpenAPI JSON]({PUBLIC_URL}/openapi.json)
- [Markdown mirror]({PUBLIC_URL}/playground.md)
- [LLM discovery]({PUBLIC_URL}/llms.txt)
- [Agent instructions]({PUBLIC_URL}/AGENTS.md)
- [Source code]({SOURCE_URL})
"""

AGENTS_MD = f"""# AGENTS.md

## Purpose
Safe Agent Playground demonstrates production boundaries for AI-agent tool execution.

## Core invariant
Model suggestion is not authorization. Authorization is enforced by deterministic application policy outside the model.

## Public API
- GET {PUBLIC_URL}/health
- POST {PUBLIC_URL}/v1/tool-check
- POST {PUBLIC_URL}/v1/run-demo
- GET {PUBLIC_URL}/openapi.json

## Safe usage
The public demo is deterministic and simulated. It performs no real notification, deletion or tenant data access. Do not send secrets, credentials, private customer data or proprietary payloads.

## Contribution source
{SOURCE_URL}
"""

PLAYGROUND_MD = f"""# Safe Agent Playground

Safe Agent Playground is an MIT-licensed FastAPI demo showing how agent tool execution can remain outside model authority.

## Live demo
{PUBLIC_URL}/

## What it demonstrates
- tenant isolation
- deterministic tool policies
- human approval gates
- destructive-action denial
- structured audit events
- correlation IDs

## Scenarios
| Scenario | Expected result |
|---|---|
| same-tenant read_record | allowed and executed |
| cross-tenant read_record | denied: tenant_mismatch |
| send_notification without approval | denied: human_approval_required |
| approved send_notification | allowed, executed and audited |
| delete_record | denied: destructive_tool_disabled_in_demo |

## Flow
`model suggestion -> policy -> approval -> execution -> audit -> correlation`

## API
- [Swagger]({PUBLIC_URL}/docs)
- [OpenAPI JSON]({PUBLIC_URL}/openapi.json)
- [Health]({PUBLIC_URL}/health)

## Source and contributions
{SOURCE_URL}
"""

HEAD_DISCOVERY_HTML = f'''\n  <meta name="description" content="Runnable open-source Safe Agent Playground demonstrating tenant isolation, deterministic tool policy, human approval, audit events and correlation IDs for AI-agent execution." />\n  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large" />\n  <link rel="canonical" href="{PUBLIC_URL}/" />\n  <link rel="describedby" href="/llms.txt" />\n  <link rel="alternate" type="text/markdown" href="/playground.md" />\n  <meta property="og:title" content="Safe Agent Playground" />\n  <meta property="og:description" content="Try deterministic agent-tool authorization, human approvals, tenant isolation and audit correlation in a runnable FastAPI demo." />\n  <meta property="og:type" content="website" />\n  <meta property="og:url" content="{PUBLIC_URL}/" />\n  <meta name="twitter:card" content="summary" />\n  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"Safe Agent Playground","description":"Runnable open-source demo for AI-agent tool authorization boundaries.","url":"{PUBLIC_URL}/","applicationCategory":"DeveloperApplication","operatingSystem":"Web","codeRepository":"{SOURCE_URL}"}}</script>\n'''
