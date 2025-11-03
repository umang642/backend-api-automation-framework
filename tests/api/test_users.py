
"""User endpoint tests (/users/{id})."""
from __future__ import annotations

import jsonschema
import pytest

from leetcode_automation.utils.schema_loader import load_schema


@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_user_by_id_schema(client, user_id):
    """Known seeded users should match the user schema."""
    r = client.get(f"/users/{user_id}")
    assert r.status_code == 200
    jsonschema.validate(instance=r.json(), schema=load_schema("user.schema.json"))


@pytest.mark.negative
def test_user_not_found(client):
    """Unknown users should return a structured 404 error body."""
    r = client.get("/users/9999")
    assert r.status_code == 404
    payload = r.json()
    assert payload["error_code"] == "USER_NOT_FOUND"
    assert "message" in payload
