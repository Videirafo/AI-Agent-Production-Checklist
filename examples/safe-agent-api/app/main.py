from fastapi import FastAPI

from app.models import (
    AuditEvent,
    RunDemoRequest,
    RunDemoResponse,
    ToolCheckRequest,
    ToolDecision,
)
from app.policy import evaluate_tool

app = FastAPI(
    title="Safe Agent API",
    version="0.2.0",
    description="Deterministic policy and audit layer for agent tool execution demos.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "safe-agent-api"}


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
def run_demo(request: RunDemoRequest) -> RunDemoResponse:
    decision = evaluate_tool(request)

    if not decision.allowed:
        return RunDemoResponse(
            request_id=request.request_id,
            decision=decision,
            executed=False,
            audit_event=build_audit_event(request, decision, executed=False),
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
        audit_event=build_audit_event(request, decision, executed=True),
    )
