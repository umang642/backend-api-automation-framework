
"""Global fixtures for the test suite.

This file defines reusable PyTest fixtures shared across all tests:

* ``base_url`` – reads the API base URL from env (``BASE_URL``) with a default.
* ``default_headers`` – attaches common test headers (e.g., trace IDs).
* ``client`` – a preconfigured :class:`HttpClient` used to make API calls.

Scopes are ``session`` so we avoid recreating the client and headers repeatedly.
"""
from __future__ import annotations

import os
import uuid

import pytest

from leetcode_automation.config import BASE_URL
from leetcode_automation.client.http_client import HttpClient


@pytest.fixture(scope="session")
def base_url() -> str:
    """Return the base URL for all API calls."""
    return os.getenv("BASE_URL", BASE_URL)


@pytest.fixture(scope="session")
def default_headers() -> dict[str, str]:
    """Return standard headers for tests.

    Includes a unique X-Request-ID per test session so logs are easy to trace.
    """
    return {
        "Accept": "application/json",
        "X-Request-ID": str(uuid.uuid4()),
    }


@pytest.fixture(scope="session")
def client(base_url: str, default_headers: dict[str, str]) -> HttpClient:
    """Create a configured :class:`HttpClient` for making API calls."""
    return HttpClient(base_url=base_url, headers=default_headers)
