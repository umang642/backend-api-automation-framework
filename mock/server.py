
"""FastAPI mock server to simulate a LeetCode-like backend.

Why this exists
---------------
A tiny, dependency-free backend lets the automation suite:
* Run locally and in CI without external services.
* Demonstrate schema/contract testing and error handling.
* Provide deterministic data via ``seed.json`` for stable assertions.
"""
from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(title="LeetCode-like API", version="1.0.0")

# Load deterministic seed so tests can assert exact values.
SEED = json.loads(Path(__file__).with_name("seed.json").read_text())


@app.get("/health")
def health():
    """Readiness probe for smoke tests and CI."""
    return {"status": "ok"}


@app.get("/problems")
def problems():
    """Return problem stats + recently solved list (from seed)."""
    return JSONResponse(content=SEED["problems"])


@app.get("/users/{id}")
def user_by_id(id: int):
    """Return a user by id or a structured 404 error."""
    for u in SEED["users"]:
        if u["id"] == id:
            return JSONResponse(content=u)
    # Use FastAPI's HTTPException to produce a 404 with a JSON body.
    raise HTTPException(
        status_code=404,
        detail={"error_code": "USER_NOT_FOUND", "message": "User not found"},
    )
