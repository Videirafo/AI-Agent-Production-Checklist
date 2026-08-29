from typing import Literal

from pydantic import BaseModel, Field

ToolName = Literal["read_record", "send_notification", "delete_record"]


class ToolCheckRequest(BaseModel):
    actor_tenant_id: str = Field(min_length=1)
    resource_tenant_id: str = Field(min_length=1)
    tool: ToolName
    human_approved: bool = False


class ToolDecision(BaseModel):
    allowed: bool
    reason: str
    requires_human_approval: bool = False


class RunDemoRequest(ToolCheckRequest):
    request_id: str = Field(min_length=1)


class RunDemoResponse(BaseModel):
    request_id: str
    decision: ToolDecision
    executed: bool
    result: str | None = None
