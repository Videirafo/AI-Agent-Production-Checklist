from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


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


def test_destructive_tool_is_disabled() -> None:
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
