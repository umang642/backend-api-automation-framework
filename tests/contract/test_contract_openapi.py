
"""Contract tests from the OpenAPI spec using Schemathesis.

These tests ensure that all endpoints described by ``mock/openapi.yaml``
conform to the declared response shapes & status codes.
"""
from __future__ import annotations

import pytest
import schemathesis

schema = schemathesis.from_path("mock/openapi.yaml")


@pytest.mark.contract
@schema.parametrize()
def test_api_contract(case):
    """Validate each endpoint/operation from the OpenAPI contract."""
    response = case.call_asgi()  # calls FastAPI app directly in memory
    case.validate_response(response)
