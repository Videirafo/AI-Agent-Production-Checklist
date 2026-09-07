PUBLIC_URL = "https://safe-agent-playground.onrender.com"
SOURCE_URL = "https://github.com/Videirafo/AI-Agent-Production-Checklist"
SOCIAL_IMAGE_URL = (
    "https://raw.githubusercontent.com/Videirafo/AI-Agent-Production-Checklist/"
    "main/assets/demo/safe-agent-playground.png"
)
RELEASE_VERSION = "0.6.0"
LAST_MODIFIED = "2026-09-07"

LLMS_TXT = f"""# Safe Agent Playground

> Runnable open-source FastAPI demo for AI-agent tool authorization boundaries. The model may suggest an action; deterministic policy and human approval decide whether execution is allowed.

## Primary resources
- [Live Playground]({PUBLIC_URL}/): interactive policy, approval, execution and audit demo
- [OpenAPI]({PUBLIC_URL}/openapi.json): machine-readable API schema
- [Swagger UI]({PUBLIC_URL}/docs): interactive API documentation
- [Playground Markdown]({PUBLIC_URL}/index.md): text-first description of the demo
- [Glossary]({PUBLIC_URL}/glossary): definitions for the safety terms used by the demo
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
  <url>
    <loc>{PUBLIC_URL}/</loc>
    <lastmod>{LAST_MODIFIED}</lastmod>
  </url>
</urlset>
"""

SITEMAP_MD = f"""# Safe Agent Playground Sitemap

## Canonical page
- [Playground]({PUBLIC_URL}/)

## Developer resources
- [OpenAPI / Swagger]({PUBLIC_URL}/docs)
- [OpenAPI JSON]({PUBLIC_URL}/openapi.json)
- [Markdown mirror]({PUBLIC_URL}/index.md)
- [Glossary]({PUBLIC_URL}/glossary)
- [LLM discovery]({PUBLIC_URL}/llms.txt)
- [Agent instructions]({PUBLIC_URL}/AGENTS.md)
- [Source code]({SOURCE_URL})
"""

AGENTS_MD = f"""# AGENTS.md

Safe Agent Playground demonstrates production boundaries for AI-agent tool execution. Core invariant: Model suggestion is not authorization. Authorization is enforced by deterministic application policy outside the model.

## Installation

Clone the source and install the example in an isolated Python environment:

```bash
git clone {SOURCE_URL}.git
cd AI-Agent-Production-Checklist/examples/safe-agent-api
python -m venv .venv
pip install -e \".[dev]\"
```

Docker is also supported through the repository's `docker compose` configuration.

## Configuration

No secrets, API keys, LLM provider, external database, or signup are required. The public demo is intentionally deterministic and simulated. Do not send credentials, private customer data, proprietary payloads, or secrets.

## Usage

Public endpoints:
- GET {PUBLIC_URL}/
- GET {PUBLIC_URL}/health
- POST {PUBLIC_URL}/v1/tool-check
- POST {PUBLIC_URL}/v1/run-demo
- GET {PUBLIC_URL}/openapi.json

The model may suggest an action, but the application policy decides whether execution is permitted.

## Examples

Use the browser Playground to run five reference scenarios: same-tenant read, cross-tenant denial, approval-required notification, approved notification, and blocked destructive delete.

For API examples and the exact schema, use {PUBLIC_URL}/docs or {PUBLIC_URL}/openapi.json.

## Contribution

Source, tests, issues, and contribution workflow: {SOURCE_URL}
"""

PLAYGROUND_MD = f"""---
title: Safe Agent Playground
description: Runnable open-source FastAPI demo for deterministic AI-agent tool authorization boundaries.
canonical: {PUBLIC_URL}/
version: {RELEASE_VERSION}
last_modified: {LAST_MODIFIED}
last_updated: {LAST_MODIFIED}
---

# Safe Agent Playground

Safe Agent Playground is an MIT-licensed FastAPI demo showing how agent tool execution can remain outside model authority. The model may suggest an action, while deterministic application policy, tenant boundaries, and human approval decide whether execution is allowed.

## Live demo

{PUBLIC_URL}/

## What it demonstrates

- tenant isolation;
- deterministic tool policies;
- human approval gates;
- destructive-action denial;
- structured audit events;
- correlation IDs;
- an execution boundary that does not depend on an LLM making its own authorization decision.

## Scenarios

| Scenario | Expected result |
|---|---|
| same-tenant read_record | allowed and executed |
| cross-tenant read_record | denied: tenant_mismatch |
| send_notification without approval | denied: human_approval_required |
| approved send_notification | allowed, executed and audited |
| delete_record | denied: destructive_tool_disabled_in_demo |

## Flow

```text
model suggestion -> policy -> approval -> execution -> audit -> correlation
```

## Glossary

- **Model suggestion:** an action proposed by an AI model; it has no execution authority by itself.
- **Tool policy:** deterministic application logic that allows or denies a proposed tool invocation.
- **Human approval:** an explicit approval signal required before selected sensitive actions can execute.
- **Tenant isolation:** the rule that an actor may only operate on resources within the permitted tenant boundary.
- **Audit event:** a structured record of the decision, execution state, reason, and correlation identifier.
- **Correlation ID:** the identifier used to connect the request, policy decision, execution result, and audit record.

Full terminology reference: {PUBLIC_URL}/glossary

## API

- [Swagger]({PUBLIC_URL}/docs)
- [OpenAPI JSON]({PUBLIC_URL}/openapi.json)
- [Health]({PUBLIC_URL}/health)

## Sitemap

- [Canonical Playground]({PUBLIC_URL}/)
- [Glossary]({PUBLIC_URL}/glossary)
- [Agent discovery]({PUBLIC_URL}/llms.txt)
- [Agent instructions]({PUBLIC_URL}/AGENTS.md)
- [Human-readable sitemap]({PUBLIC_URL}/sitemap.md)

## Source and contributions

{SOURCE_URL}
"""

GLOSSARY_MD = f"""---
title: Safe Agent Playground Glossary
description: Definitions for the production-safety terms used by Safe Agent Playground.
canonical: {PUBLIC_URL}/glossary
last_updated: {LAST_MODIFIED}
---

# Safe Agent Playground Glossary

## Model suggestion
An action proposed by a model. A suggestion is input to policy evaluation and never grants execution authority by itself.

## Tool policy
Deterministic application logic that evaluates a proposed tool action against tenant scope, approval requirements, and disabled-action rules.

## Human approval
An explicit approval signal required for selected sensitive tools. Approval is necessary where policy requires it, but approval does not override a policy that disables an action.

## Tenant isolation
The boundary that prevents an actor in one tenant from operating on a resource that belongs to another tenant.

## Audit event
A structured record capturing the correlation ID, actor tenant, resource tenant, tool, policy decision, execution state, reason, and approval state.

## Correlation ID
A request identifier used to connect a user-visible request with its policy decision, execution result, and audit record.

## Destructive action
An operation that can delete or irreversibly change data. The public demo deliberately blocks destructive execution even when human approval is present.

## Related resources
- [Live Playground]({PUBLIC_URL}/)
- [OpenAPI]({PUBLIC_URL}/openapi.json)
- [Agent instructions]({PUBLIC_URL}/AGENTS.md)
- [Source]({SOURCE_URL})
"""

GLOSSARY_HTML = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Safe Agent Playground Glossary</title>
  <meta name="description" content="Definitions for tenant isolation, tool policy, human approval, audit events, correlation IDs, and other Safe Agent Playground terms." />
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large" />
  <link rel="canonical" href="{PUBLIC_URL}/glossary" />
  <link rel="describedby" href="/llms.txt" />
  <link rel="alternate" type="text/markdown" href="/glossary.md" />
  <meta property="og:title" content="Safe Agent Playground Glossary" />
  <meta property="og:description" content="Definitions for the production-safety terms used by Safe Agent Playground." />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{PUBLIC_URL}/glossary" />
  <style>body{{margin:0;font:16px/1.65 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:#08111f;color:#e8eef7}}main{{max-width:820px;margin:auto;padding:44px 20px 72px}}a{{color:#68a7ff}}h1{{font-size:42px;line-height:1.1}}h2{{margin-top:30px}}p{{color:#c6d2e1}}</style>
</head>
<body>
<main>
  <p><a href="/">← Back to Safe Agent Playground</a></p>
  <h1>Safe Agent Playground Glossary</h1>
  <p>This glossary defines the production-safety terms used by the Playground so readers, search systems, and AI agents can resolve the architecture consistently.</p>
  <h2>Model suggestion</h2><p>An action proposed by a model. It is evaluated as untrusted input and never grants execution authority by itself.</p>
  <h2>Tool policy</h2><p>Deterministic application logic that evaluates tenant scope, approval requirements, and disabled-action rules before execution.</p>
  <h2>Human approval</h2><p>An explicit approval signal required for selected sensitive operations. Approval can satisfy a policy requirement but cannot bypass a policy that disables an action.</p>
  <h2>Tenant isolation</h2><p>The boundary preventing an actor associated with one tenant from operating on resources belonging to another tenant.</p>
  <h2>Audit event</h2><p>A structured record of the policy decision and execution state, including reason, tenant context, approval state, and correlation identifier.</p>
  <h2>Correlation ID</h2><p>A request identifier used to connect a request with its policy decision, execution result, and audit event.</p>
  <h2>Destructive action</h2><p>An operation capable of irreversible or high-impact change. The public demo blocks destructive execution even when human approval is present.</p>
</main>
</body>
</html>'''

HEAD_DISCOVERY_HTML = f'''\n  <meta name="description" content="Runnable open-source Safe Agent Playground demonstrating tenant isolation, deterministic tool policy, human approval, audit events and correlation IDs for AI-agent execution." />\n  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large" />\n  <link rel="canonical" href="{PUBLIC_URL}/" />\n  <link rel="describedby" href="/llms.txt" />\n  <link rel="alternate" type="text/markdown" href="/index.md" />\n  <meta property="og:title" content="Safe Agent Playground" />\n  <meta property="og:description" content="Try deterministic agent-tool authorization, human approvals, tenant isolation and audit correlation in a runnable FastAPI demo." />\n  <meta property="og:type" content="website" />\n  <meta property="og:url" content="{PUBLIC_URL}/" />\n  <meta property="og:image" content="{SOCIAL_IMAGE_URL}" />\n  <meta name="twitter:card" content="summary_large_image" />\n  <meta name="twitter:title" content="Safe Agent Playground" />\n  <meta name="twitter:description" content="Runnable open-source demo for AI-agent tool authorization boundaries." />\n  <meta name="twitter:image" content="{SOCIAL_IMAGE_URL}" />\n  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"Safe Agent Playground","headline":"Safe Agent Playground","description":"Runnable open-source demo for AI-agent tool authorization boundaries.","url":"{PUBLIC_URL}/","dateModified":"{LAST_MODIFIED}","softwareVersion":"{RELEASE_VERSION}","applicationCategory":"DeveloperApplication","operatingSystem":"Web","codeRepository":"{SOURCE_URL}"}}</script>\n'''

DISCOVERY_BODY_HTML = f'''\n    <section class="card" style="margin-top:20px" aria-labelledby="why-title">\n      <h2 id="why-title">Why this demo exists</h2>\n      <p>Many AI-agent examples demonstrate how a model selects or calls a tool, but production systems need a separate authorization boundary. This Playground makes that boundary visible: tenant scope is checked first, sensitive actions can require human approval, destructive actions remain blocked, and every decision can be correlated with an audit event.</p>\n      <h3>What to evaluate</h3>\n      <p>Try an allowed same-tenant read, then change the resource tenant and observe the denial. Compare a notification request before and after human approval. Finally, try the destructive delete scenario and verify that approval alone cannot bypass a policy that disables the tool. The purpose is not to simulate intelligence; it is to make execution policy deterministic, inspectable, testable, and independent from model persuasion.</p>\n      <h3>Why the boundary matters</h3>\n      <p>Agent systems become safer when model output is treated as a proposal rather than a permission grant. A separate policy layer can enforce tenant isolation, require approval for sensitive capabilities, disable destructive tools, and record the decision independently of the model's wording. That separation makes the behavior easier to test, audit, review, and reproduce across model providers.</p>\n      <p>The demo intentionally performs simulated actions only, so visitors can inspect an allowed execution and several denial paths without credentials, private data, or external side effects. See the <a href="/glossary">glossary</a> for definitions of model suggestion, tool policy, human approval, tenant isolation, audit event, correlation ID, and destructive action.</p>\n      <p>Machine-readable resources are available through <a href="/openapi.json">OpenAPI</a>, <a href="/llms.txt">llms.txt</a>, <a href="/AGENTS.md">AGENTS.md</a>, and the <a href="/index.md">Markdown mirror</a>.</p>\n    </section>\n'''
