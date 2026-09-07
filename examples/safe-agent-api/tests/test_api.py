from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_playground_is_public_and_self_contained() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Safe Agent Playground" in response.text
    assert "/v1/run-demo" in response.text
    assert "Why this demo exists" in response.text
    assert 'rel="canonical"' in response.text
    assert 'rel="describedby" href="/llms.txt"' in response.text
    assert 'property="og:title"' in response.text
    assert 'type="application/ld+json"' in response.text
    assert response.headers["x-content-type-options"] == "nosniff"
    assert "connect-src 'self'" in response.headers["content-security-policy"]
    assert response.headers["x-robots-tag"].startswith("index, follow")


def test_head_root_is_supported() -> None:
    response = client.head("/")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")


def test_root_supports_markdown_content_negotiation() -> None:
    response = client.get("/", headers={"Accept": "text/markdown"})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/markdown")
    assert "# Safe Agent Playground" in response.text
    assert "## Sitemap" in response.text
    assert 'rel="canonical"' in response.headers["link"]


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "safe-agent-api",
        "version": "0.6.0",
    }


def test_discovery_documents_are_public() -> None:
    llms = client.get("/llms.txt")
    assert llms.status_code == 200
    assert llms.headers["content-type"].startswith("text/plain")
    assert "# Safe Agent Playground" in llms.text
    assert "/openapi.json" in llms.text
    assert "/index.md" in llms.text

    full = client.get("/llms-full.txt")
    assert full.status_code == 200
    assert "## Demo scenarios" in full.text

    robots = client.get("/robots.txt")
    assert robots.status_code == 200
    assert "User-agent: *" in robots.text
    assert "Sitemap:" in robots.text

    sitemap_xml = client.get("/sitemap.xml")
    assert sitemap_xml.status_code == 200
    assert sitemap_xml.headers["content-type"].startswith("application/xml")
    assert "<urlset" in sitemap_xml.text
    assert "<lastmod>2026-09-07</lastmod>" in sitemap_xml.text
    assert "<loc>https://safe-agent-playground.onrender.com/</loc>" in sitemap_xml.text
    assert "playground.md" not in sitemap_xml.text

    sitemap_md = client.get("/sitemap.md")
    assert sitemap_md.status_code == 200
    assert sitemap_md.headers["content-type"].startswith("text/markdown")

    agents = client.get("/AGENTS.md")
    assert agents.status_code == 200
    assert "Model suggestion is not authorization" in agents.text
    assert "## Installation" in agents.text
    assert "## Configuration" in agents.text
    assert "## Usage" in agents.text
    assert "## Examples" in agents.text

    markdown = client.get("/index.md")
    assert markdown.status_code == 200
    assert markdown.headers["content-type"].startswith("text/markdown")
    assert markdown.text.startswith("---\n")
    assert "canonical: https://safe-agent-playground.onrender.com/" in markdown.text
    assert "last_modified: 2026-09-07" in markdown.text
    assert "## Scenarios" in markdown.text
    assert "## Sitemap" in markdown.text


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
