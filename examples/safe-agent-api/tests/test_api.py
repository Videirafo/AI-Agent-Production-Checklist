from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_playground_is_public_and_self_contained() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Safe Agent Playground" in response.text
    assert "/v1/run-demo" in response.text
    assert response.headers["x-content-type-options"] == "nosniff"
    assert "connect-src 'self'" in response.headers["content-security-policy"]


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "safe-agent-api",
        "version": "0.5.0",
    }


def test_read_is_allowed_in_same_tenant() -> None:
    response = client.post(
        "/v1/tool-check",
        json={
            "actor_tenant_id": "alpha",
            "resource_tenant_id": "alpha",
            "tool": "read_record",
            "human_approved": False,
        },
    )
    assert response.status_code == 200
    assert response.json()["allowed"] is True


def test_cross_tenant_access_is_denied() -> None:
    response = client.post(
        "/v1/tool-check",
        json={
            "actor_tenant_id": "alpha",
            "resource_tenant_id": "beta",
            "tool": "read_record",
            "human_approved": False,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "allowed": False,
        "reason": "tenant_mismatch",
        "requires_human_approval": False,
    }


def test_notification_requires_human_approval() -> None:
    response = client.post(
        "/v1/tool-check",
        json={
            "actor_tenant_id": "alpha",
            "resource_tenant_id": "alpha",
            "tool": "send_notification",
            "human_approved": False,
        },
    )
    body = response.json()
    assert body["allowed"] is False
    assert body["requires_human_approval"] is True


def test_public_input_is_bounded() -> None:
    response = client.post(
        "/v1/tool-check",
        json={
            "actor_tenant_id": "a" * 65,
            "resource_tenant_id": "alpha",
            "tool": "read_record",
            "human_approved": False,
        },
    )
    assert response.status_code == 422


def test_destructive_tool_denial_is_correlated_in_audit_event() -> None:
    response = client.post(
        "/v1/run-demo",
        json={
            "request_id": "req-demo-001",
            "actor_tenant_id": "alpha",
            "resource_tenant_id": "alpha",
            "tool": "delete_record",
            "human_approved": True,
        },
    )
    body = response.json()
    assert body["executed"] is False
    assert body["decision"]["reason"] == "destructive_tool_disabled_in_demo"
    assert body["audit_event"]["correlation_id"] == "req-demo-001"
    assert body["audit_event"]["allowed"] is False
    assert body["audit_event"]["executed"] is False


def test_approved_notification_execution_is_audited() -> None:
    response = client.post(
        "/v1/run-demo",
        json={
            "request_id": "req-demo-002",
            "actor_tenant_id": "alpha",
            "resource_tenant_id": "alpha",
            "tool": "send_notification",
            "human_approved": True,
        },
    )
    body = response.json()
    assert body["executed"] is True
    assert body["result"] == "demo_notification_sent"
    assert body["audit_event"] == {
        "event_type": "tool_execution_decision",
        "correlation_id": "req-demo-002",
        "actor_tenant_id": "alpha",
        "resource_tenant_id": "alpha",
        "tool": "send_notification",
        "allowed": True,
        "executed": True,
        "reason": "policy_allowed",
        "human_approved": True,
    }
