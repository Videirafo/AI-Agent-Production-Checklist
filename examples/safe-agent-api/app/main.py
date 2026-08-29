from fastapi import FastAPI

from app.models import RunDemoRequest, RunDemoResponse, ToolCheckRequest, ToolDecision
from app.policy import evaluate_tool

app = FastAPI(
    title="Safe Agent API",
    version="0.1.0",
    description="Deterministic policy layer for agent tool execution demos.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "safe-agent-api"}


@app.post("/v1/tool-check", response_model=ToolDecision)
def tool_check(request: ToolCheckRequest) -> ToolDecision:
    return evaluate_tool(request)


@app.post("/v1/run-demo", response_model=RunDemoResponse)
def run_demo(request: RunDemoRequest) -> RunDemoResponse:
    decision = evaluate_tool(request)

    if not decision.allowed:
        return RunDemoResponse(
            request_id=request.request_id,
            decision=decision,
            executed=False,
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
    )
