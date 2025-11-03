
"""Schema loading helpers.

Why this exists
---------------
Tests often validate responses against JSON Schemas. Centralizing the loading
logic keeps tests clean and makes path resolution consistent.
"""
from __future__ import annotations

import json
from pathlib import Path


def load_schema(name: str) -> dict:
    """Load a JSON Schema from ``tests/schemas/<name>``.

    Parameters
    ----------
    name:
        File name of the schema (e.g., ``"user.schema.json"``).

    Returns
    -------
    dict
        Parsed JSON schema dictionary.
    """
    # Navigate up to project root and into tests/schemas.
    path = Path(__file__).resolve().parents[3] / "tests" / "schemas" / name
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
