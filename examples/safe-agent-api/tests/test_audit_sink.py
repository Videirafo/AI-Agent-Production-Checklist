import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.audit import JsonlAuditSink, get_audit_sink
from app.main import app

client = TestClient(app)


def _run_demo(payload: dict[str, object]) -> None:
    response = client.post("/v1/run-demo", json=payload)
    assert response.status_code == 200


def test_jsonl_sink_persists_allowed_and_denied_decisions(tmp_path: Path) -> None:
    audit_path = tmp_path / "audit" / "events.jsonl"
    app.dependency_overrides[get_audit_sink] = lambda: JsonlAuditSink(audit_path)

    try:
        _run_demo(
            {
                "request_id": "req-jsonl-allowed",
                "actor_tenant_id": "alpha",
                "resource_tenant_id": "alpha",
                "tool": "read_record",
                "human_approved": False,
            }
        )
        _run_demo(
            {
                "request_id": "req-jsonl-denied",
                "actor_tenant_id": "alpha",
                "resource_tenant_id": "beta",
                "tool": "read_record",
                "human_approved": False,
            }
        )
    finally:
        app.dependency_overrides.clear()

    rows = [json.loads(line) for line in audit_path.read_text(encoding="utf-8").splitlines()]

    assert len(rows) == 2
    assert rows[0]["correlation_id"] == "req-jsonl-allowed"
    assert rows[0]["allowed"] is True
    assert rows[0]["executed"] is True
    assert rows[1]["correlation_id"] == "req-jsonl-denied"
    assert rows[1]["allowed"] is False
    assert rows[1]["executed"] is False
    assert rows[1]["reason"] == "tenant_mismatch"

    forbidden_keys = {"prompt", "conversation", "secret", "payload"}
    assert all(forbidden_keys.isdisjoint(row) for row in rows)
