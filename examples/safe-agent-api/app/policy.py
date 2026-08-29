from app.models import ToolCheckRequest, ToolDecision


def evaluate_tool(request: ToolCheckRequest) -> ToolDecision:
    if request.actor_tenant_id != request.resource_tenant_id:
        return ToolDecision(
            allowed=False,
            reason="tenant_mismatch",
        )

    if request.tool == "delete_record":
        return ToolDecision(
            allowed=False,
            reason="destructive_tool_disabled_in_demo",
        )

    if request.tool == "send_notification" and not request.human_approved:
        return ToolDecision(
            allowed=False,
            reason="human_approval_required",
            requires_human_approval=True,
        )

    return ToolDecision(
        allowed=True,
        reason="policy_allowed",
    )
