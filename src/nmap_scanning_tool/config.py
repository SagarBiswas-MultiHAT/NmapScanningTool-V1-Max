"""Application configuration sourced from environment variables."""

from __future__ import annotations

import os

DEFAULT_PORT_RANGE = "1-65535"
DEFAULT_NMAP_BINARY = "nmap"


def get_nmap_binary() -> str:
    """Return the Nmap binary path/name from env or default value."""
    value = os.getenv("NMAP_BINARY", DEFAULT_NMAP_BINARY).strip()
    return value or DEFAULT_NMAP_BINARY


def get_default_ports() -> str:
    """Return default port range from env or sensible fallback."""
    value = os.getenv("NMAP_DEFAULT_PORTS", DEFAULT_PORT_RANGE).strip()
    return value or DEFAULT_PORT_RANGE
