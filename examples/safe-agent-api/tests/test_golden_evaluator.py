from pathlib import Path

from app.task_contract import (
    GoldenCase,
    GoldenSuite,
    evaluate_golden_case,
    evaluate_golden_suite,
)

FIXTURE = Path(__file__).resolve().parents[1] / "evals" / "golden_cases.json"


def load_suite() -> GoldenSuite:
    return GoldenSuite.model_validate_json(FIXTURE.read_text(encoding="utf-8"))


def test_golden_policy_suite_passes() -> None:
    suite = load_suite()
    results = evaluate_golden_suite(suite)

    assert len(results) == 5
    assert all(result.passed for result in results)
    assert {result.terminal_state for result in results} == {
        "PASS",
        "BLOCKED",
        "NEEDS_HUMAN",
    }
    assert all(result.observed_turns <= suite.contract.budget.max_turns for result in results)
    assert all(
        result.observed_tool_calls <= suite.contract.budget.max_tool_calls
        for result in results
    )


def test_golden_evaluator_reports_intentional_mismatch() -> None:
    suite = load_suite()
    source = next(case for case in suite.cases if case.id == "cross-tenant-read")
    payload = source.model_dump()
    payload["expected"]["terminal_state"] = "PASS"
    mismatched = GoldenCase.model_validate(payload)

    result = evaluate_golden_case(suite.contract, mismatched)

    assert result.passed is False
    assert result.terminal_state == "BLOCKED"
    assert any("terminal_state" in failure for failure in result.failed_criteria)
