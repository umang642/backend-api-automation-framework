
"""Smoke tests for the service readiness endpoint (/health)."""
from __future__ import annotations

import pytest


@pytest.mark.smoke
def test_health_ok(client):
    """Service should report a simple OK status for readiness probes."""
    r = client.get("/health")
    assert r.status_code == 200

    body = r.json()
    # Minimal contract: presence of a 'status' key with value 'ok'.
    assert body.get("status") == "ok"
