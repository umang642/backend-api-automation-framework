
"""Functional tests for /problems endpoint.

Covers:
* JSON Schema validation
* Domain sanity checks (counts, ranges, enum values)
* Ordering constraints (timestamps newest-first)
"""
from __future__ import annotations

import jsonschema

from leetcode_automation.utils.schema_loader import load_schema
from leetcode_automation.utils.validators import is_iso_utc, not_future


def test_problems_list_schema(client):
    """Response must conform to the agreed JSON Schema."""
    r = client.get("/problems")
    assert r.status_code == 200
    jsonschema.validate(instance=r.json(), schema=load_schema("problems_list.schema.json"))


def test_problems_constraints(client):
    """Validate business logic and data ranges on problem stats and list."""
    body = client.get("/problems").json()

    # Totals should be coherent: solved never exceeds total.
    assert body["num_total"] >= 0
    assert 0 <= body["num_solved"] <= body["num_total"]

    # Recently solved should be a list of well-formed items.
    probs = body["recently_solved"]
    assert isinstance(probs, list)
    for p in probs:
        assert p["difficulty"] in {"Easy", "Medium", "Hard"}
        # Timestamps must be ISO-UTC and not in the future.
        assert is_iso_utc(p["timestamp"]) and not_future(p["timestamp"])


def test_problems_sorted_desc(client):
    """Recently solved items must be sorted descending by timestamp."""
    items = client.get("/problems").json()["recently_solved"]
    ts = [i["timestamp"] for i in items]
    assert ts == sorted(ts, reverse=True)
