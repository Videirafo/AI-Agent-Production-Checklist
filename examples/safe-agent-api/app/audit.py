from __future__ import annotations

import os
from pathlib import Path
from typing import Protocol

from app.models import AuditEvent


class AuditSink(Protocol):
    """Narrow persistence boundary for validated audit events."""

    def write(self, event: AuditEvent) -> None:
        """Persist one validated audit event."""


class NullAuditSink:
    """Default sink: keep the public demo stateless unless explicitly configured."""

    def write(self, event: AuditEvent) -> None:
        del event


class JsonlAuditSink:
    """Dependency-light file sink for local demos and tests, not production storage."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def write(self, event: AuditEvent) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(event.model_dump_json())
            handle.write("\n")


def get_audit_sink() -> AuditSink:
    path = os.getenv("SAFE_AGENT_AUDIT_JSONL_PATH", "").strip()
    if not path:
        return NullAuditSink()
    return JsonlAuditSink(path)
