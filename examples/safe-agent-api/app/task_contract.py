from __future__ import annotations

from time import perf_counter
from typing import Literal

from pydantic import BaseModel, Field

from app.models import RunDemoRequest, ToolDecision
from app.policy import evaluate_tool

TaskTerminalState = Literal[
    "PASS",
    "FAIL",
    "RETRYABLE",
    "BLOCKED",
    "NEEDS_HUMAN",
]


class TaskBudget(BaseModel):
    max_turns: int = Field(default=1, ge=1, le=64)
    max_tool_calls: int = Field(default=1, ge=0, le=64)
    max_time_ms: int = Field(default=1_000, ge=1, le=120_000)


class TaskContract(BaseModel):
    id: str = Field(min_length=3, max_length=80, pattern=r"^[a-z0-9][a-z0-9._-]+$")
    objective: str = Field(min_length=3, max_length=240)
    success_criteria: list[str] = Field(min_length=1, max_length=16)
    stop_criteria: list[str] = Field(min_length=1, max_length=16)
    budget: TaskBudget = Field(default_factory=TaskBudget)


class GoldenExpectation(BaseModel):
    terminal_state: TaskTerminalState
    allowed: bool
    executed: bool
    reason: str = Field(min_length=1, max_length=120)
    requires_human_approval: bool = False


class GoldenCase(BaseModel):
    id: str = Field(min_length=3, max_length=80, pattern=r"^[a-z0-9][a-z0-9._-]+$")
    request: RunDemoRequest
    expected: GoldenExpectation


class GoldenSuite(BaseModel):
    contract: TaskContract
    cases: list[GoldenCase] = Field(min_length=1, max_length=100)


class TaskEvaluation(BaseModel):
    case_id: str
    passed: bool
    terminal_state: TaskTerminalState
    failed_criteria: list[str]
    observed_turns: int
    observed_tool_calls: int
    elapsed_ms: float
    decision: ToolDecision
    executed: bool


def terminal_state_for(decision: ToolDecision) -> TaskTerminalState:
    if decision.allowed:
        return "PASS"
    if decision.reason == "human_approval_required":
        return "NEEDS_HUMAN"
    if decision.reason in {
        "tenant_mismatch",
        "destructive_tool_disabled_in_demo",
    }:
        return "BLOCKED"
    return "FAIL"


def evaluate_golden_case(contract: TaskContract, case: GoldenCase) -> TaskEvaluation:
    started = perf_counter()
    decision = evaluate_tool(case.request)
    executed = decision.allowed
    terminal_state = terminal_state_for(decision)
    elapsed_ms = (perf_counter() - started) * 1_000

    observed_turns = 1
    observed_tool_calls = 1 if executed else 0
    failed: list[str] = []

    expected = case.expected
    observations = {
        "terminal_state": terminal_state,
        "allowed": decision.allowed,
        "executed": executed,
        "reason": decision.reason,
        "requires_human_approval": decision.requires_human_approval,
    }
    expected_values = expected.model_dump()

    for key, actual in observations.items():
        wanted = expected_values[key]
        if actual != wanted:
            failed.append(f"{key}: expected {wanted!r}, got {actual!r}")

    if observed_turns > contract.budget.max_turns:
        failed.append("budget.max_turns exceeded")
    if observed_tool_calls > contract.budget.max_tool_calls:
        failed.append("budget.max_tool_calls exceeded")
    if elapsed_ms > contract.budget.max_time_ms:
        failed.append("budget.max_time_ms exceeded")

    return TaskEvaluation(
        case_id=case.id,
        passed=not failed,
        terminal_state=terminal_state,
        failed_criteria=failed,
        observed_turns=observed_turns,
        observed_tool_calls=observed_tool_calls,
        elapsed_ms=elapsed_ms,
        decision=decision,
        executed=executed,
    )


def evaluate_golden_suite(suite: GoldenSuite) -> list[TaskEvaluation]:
    return [evaluate_golden_case(suite.contract, case) for case in suite.cases]
