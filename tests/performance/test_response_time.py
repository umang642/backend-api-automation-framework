
"""Lightweight performance guardrails for /problems endpoint."""
from __future__ import annotations

import pytest


@pytest.mark.perf
def test_problems_response_time(client):
    """Basic SLA: response should be timely and payload not excessive."""
    r = client.get("/problems")
    # Keep response under 1.5s in CI; adjust as needed per environment.
    assert r.elapsed.total_seconds() < 1.5
    # Guardrail for accidental payload bloat.
    assert len(r.content) < 500_000  # < 500 KB
