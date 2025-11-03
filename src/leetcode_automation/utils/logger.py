
"""Minimal console logger utilities using Rich.

Why this exists
---------------
In test suites, printing raw dicts is hard to read. These helpers render
key/value pairs as a simple table so CI logs are human‑friendly.
"""
from __future__ import annotations

from rich.console import Console
from rich.table import Table

console = Console()


def log_kv(title: str, **kwargs) -> None:
    """Render a titled key/value table to the console.

    Examples
    --------
    >>> log_kv("Request Context", method="GET", path="/problems", req_id="123")
    """
    table = Table(title=title)
    table.add_column("Key")
    table.add_column("Value")
    for k, v in kwargs.items():
        table.add_row(str(k), str(v))
    console.print(table)
