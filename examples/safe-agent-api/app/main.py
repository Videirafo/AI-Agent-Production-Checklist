from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, Response

from app.audit import AuditSink, get_audit_sink
from app.discovery import (
    AGENTS_MD,
    DISCOVERY_BODY_HTML,
    GLOSSARY_HTML,
    GLOSSARY_MD,
    HEAD_DISCOVERY_HTML,
    LLMS_FULL_TXT,
    LLMS_TXT,
    PLAYGROUND_MD,
    RELEASE_VERSION,
    ROBOTS_TXT,
    SITEMAP_MD,
    SITEMAP_XML,
)
from app.models import (
    AuditEvent,
    RunDemoRequest,
    RunDemoResponse,
    ToolCheckRequest,
    ToolDecision,
)
from app.playground import PLAYGROUND_HTML
from app.policy import evaluate_tool

app = FastAPI(
    title="Safe Agent API",
    version=RELEASE_VERSION,
    description="Deterministic policy, approval and audit layer for agent tool execution demos.",
)


MARKDOWN_HEADERS = {
    "Link": '</>; rel="canonical", </sitemap.md>; rel="sitemap"',
    "X-Robots-Tag": "index, follow, max-snippet:-1, max-image-preview:large",
}


@app.api_route("/", methods=["GET", "HEAD"], response_class=HTMLResponse, include_in_schema=False)
def playground(request: Request) -> Response:
    accept = request.headers.get("accept", "").lower()
    if request.method == "GET" and "text/markdown" in accept:
        return PlainTextResponse(
            PLAYGROUND_MD,
            media_type="text/markdown",
            headers=MARKDOWN_HEADERS,
        )

    html = PLAYGROUND_HTML.replace("</head>", f"{HEAD_DISCOVERY_HTML}</head>")
    html = html.replace('<p class="footer">', f'{DISCOVERY_BODY_HTML}<p class="footer">')
    return HTMLResponse(
        html,
        headers={
            "Cache-Control": "no-store",
            "Content-Security-Policy": (
                "default-src 'self'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; "
                "connect-src 'self'; img-src 'self' data: https://raw.githubusercontent.com; "
                "frame-ancestors 'none'"
            ),
            "Link": '</llms.txt>; rel="describedby", </index.md>; rel="alternate"; type="text/markdown"',
            "Referrer-Policy": "no-referrer",
            "X-Content-Type-Options": "nosniff",
            "X-Robots-Tag": "index, follow, max-snippet:-1, max-image-preview:large",
        },
    )


@app.get("/glossary", response_class=HTMLResponse, include_in_schema=False)
def glossary() -> HTMLResponse:
    return HTMLResponse(
        GLOSSARY_HTML,
        headers={
            "Cache-Control": "public, max-age=300",
            "Content-Security-Policy": "default-src 'self'; style-src 'unsafe-inline'; frame-ancestors 'none'",
            "Link": '</llms.txt>; rel="describedby", </glossary.md>; rel="alternate"; type="text/markdown"',
            "Referrer-Policy": "no-referrer",
            "X-Content-Type-Options": "nosniff",
            "X-Robots-Tag": "index, follow, max-snippet:-1, max-image-preview:large",
        },
    )


@app.get("/glossary.md", response_class=PlainTextResponse, include_in_schema=False)
def glossary_md() -> PlainTextResponse:
    return PlainTextResponse(
        GLOSSARY_MD,
        media_type="text/markdown",
        headers={
            "Link": '</glossary>; rel="canonical", </sitemap.md>; rel="sitemap"',
            "X-Robots-Tag": "index, follow, max-snippet:-1, max-image-preview:large",
        },
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "safe-agent-api", "version": RELEASE_VERSION}


@app.get("/llms.txt", response_class=PlainTextResponse, include_in_schema=False)
def llms_txt() -> PlainTextResponse:
    return PlainTextResponse(LLMS_TXT, media_type="text/plain")


@app.get("/llms-full.txt", response_class=PlainTextResponse, include_in_schema=False)
def llms_full_txt() -> PlainTextResponse:
    return PlainTextResponse(LLMS_FULL_TXT, media_type="text/plain")


@app.get("/robots.txt", response_class=PlainTextResponse, include_in_schema=False)
def robots_txt() -> PlainTextResponse:
    return PlainTextResponse(ROBOTS_TXT, media_type="text/plain")


@app.get("/sitemap.xml", include_in_schema=False)
def sitemap_xml() -> Response:
    return Response(SITEMAP_XML, media_type="application/xml")


@app.get("/sitemap.md", response_class=PlainTextResponse, include_in_schema=False)
def sitemap_md() -> PlainTextResponse:
    return PlainTextResponse(SITEMAP_MD, media_type="text/markdown")


@app.get("/AGENTS.md", response_class=PlainTextResponse, include_in_schema=False)
def agents_md() -> PlainTextResponse:
    return PlainTextResponse(AGENTS_MD, media_type="text/markdown")


@app.get("/index.md", response_class=PlainTextResponse, include_in_schema=False)
@app.get("/playground.md", response_class=PlainTextResponse, include_in_schema=False)
def playground_md() -> PlainTextResponse:
    return PlainTextResponse(
        PLAYGROUND_MD,
        media_type="text/markdown",
        headers=MARKDOWN_HEADERS,
    )


@app.post("/v1/tool-check", response_model=ToolDecision)
def tool_check(request: ToolCheckRequest) -> ToolDecision:
    return evaluate_tool(request)


def build_audit_event(
    request: RunDemoRequest,
    decision: ToolDecision,
    executed: bool,
) -> AuditEvent:
    return AuditEvent(
        correlation_id=request.request_id,
        actor_tenant_id=request.actor_tenant_id,
        resource_tenant_id=request.resource_tenant_id,
        tool=request.tool,
        allowed=decision.allowed,
        executed=executed,
        reason=decision.reason,
        human_approved=request.human_approved,
    )


@app.post("/v1/run-demo", response_model=RunDemoResponse)
def run_demo(
    request: RunDemoRequest,
    audit_sink: AuditSink = Depends(get_audit_sink),
) -> RunDemoResponse:
    decision = evaluate_tool(request)
    executed = decision.allowed
    audit_event = build_audit_event(request, decision, executed=executed)

    # Persist only the validated, bounded AuditEvent after policy is known.
    audit_sink.write(audit_event)

    if not decision.allowed:
        return RunDemoResponse(
            request_id=request.request_id,
            decision=decision,
            executed=False,
            audit_event=audit_event,
        )

    simulated_result = {
        "read_record": "demo_record_returned",
        "send_notification": "demo_notification_sent",
    }.get(request.tool, "no_action")

    return RunDemoResponse(
        request_id=request.request_id,
        decision=decision,
        executed=True,
        result=simulated_result,
        audit_event=audit_event,
    )
