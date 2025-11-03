
"""HTTP client utilities for API tests.

This module exposes :class:`HttpClient`, a thin wrapper around ``requests.Session``
to standardize how API tests perform HTTP calls.

Why this exists
---------------
* Provide a single place for base URL handling (so tests just pass relative paths).
* Apply a consistent retry strategy for transient HTTP errors / rate limits.
* Share a persistent session across requests for connection reuse & performance.
* Centralize default headers and default timeouts.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from leetcode_automation.config import DEFAULT_TIMEOUT


class HttpClient:
    """Reusable HTTP client used by tests.

    The client wraps a ``requests.Session`` and exposes convenience methods for
    common HTTP verbs. It also sets up a retry policy so your tests are more
    resilient to transient failures (e.g., 429, 5xx).

    Parameters
    ----------
    base_url:
        The API base URL; a trailing slash is stripped to keep URL joins clean.
    headers:
        Optional default headers that will be attached to every request.
    timeout:
        Default per‑request timeout (in seconds). Can be overridden per call.
    """

    def __init__(
        self,
        base_url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        # Normalize the base URL so later we can safely join with relative paths.
        self.base_url = base_url.rstrip("/")

        # A single session is kept for connection pooling & cookie persistence.
        self.session = requests.Session()
        self.session.headers.update(headers or {})

        # Configure a conservative retry policy for flaky networks or 5xx bursts.
        retries = Retry(
            total=3,                       # up to 3 total retries
            backoff_factor=0.3,            # exponential backoff (0.3, 0.6, 1.2s)
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=frozenset({    # which HTTP methods are retried
                "GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"
            }),
            raise_on_status=False,         # don't raise, return the response
            respect_retry_after_header=True,
        )

        # Mount retry‑enabled adapters for both HTTP and HTTPS.
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Default timeout can be overridden on each call.
        self.timeout = timeout

    # ----------------------------- Internal helpers -----------------------------
    def _url(self, path: str) -> str:
        """Join ``base_url`` with a relative ``path`` safely."""
        return f"{self.base_url}/{path.lstrip('/')}"

    # ------------------------------ Public methods ------------------------------
    def get(self, path: str, **kwargs) -> requests.Response:
        """Perform a GET request to ``base_url + path``.

        Extra ``kwargs`` are forwarded to ``requests.Session.get``. To override
        the timeout for a single request, pass ``timeout=<seconds>``.
        """
        return self.session.get(self._url(path), timeout=self.timeout, **kwargs)

    def post(self, path: str, json: Any | None = None, **kwargs) -> requests.Response:
        """Perform a POST request with an optional JSON body."""
        return self.session.post(self._url(path), json=json, timeout=self.timeout, **kwargs)

    def put(self, path: str, json: Any | None = None, **kwargs) -> requests.Response:
        """Perform a PUT request with an optional JSON body."""
        return self.session.put(self._url(path), json=json, timeout=self.timeout, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        """Perform a DELETE request."""
        return self.session.delete(self._url(path), timeout=self.timeout, **kwargs)
