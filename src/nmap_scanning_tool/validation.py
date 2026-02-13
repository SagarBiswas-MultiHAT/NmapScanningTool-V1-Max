"""Validation helpers for user-provided targets, ports, and custom arguments."""

from __future__ import annotations

import ipaddress
import re
from collections.abc import Sequence

from .errors import ValidationError

_HOSTNAME_PATTERN = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(?:\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*$"
)
_PORT_LIST_PATTERN = re.compile(r"^\d{1,5}(?:-\d{1,5})?(?:,\d{1,5}(?:-\d{1,5})?)*$")


def validate_target(target: str) -> str:
    """Validate IPv4/IPv6 or hostname targets accepted by Nmap."""
    normalized = target.strip()
    if not normalized:
        raise ValidationError("Target cannot be empty.")

    try:
        ipaddress.ip_address(normalized)
        return normalized
    except ValueError:
        if _HOSTNAME_PATTERN.fullmatch(normalized):
            return normalized

    raise ValidationError("Target must be a valid IPv4/IPv6 address or RFC-compliant hostname.")


def validate_ports(ports: str) -> str:
    """Validate Nmap-compatible port strings containing integers and ranges."""
    normalized = ports.strip()
    if not normalized:
        raise ValidationError("Port selection cannot be empty.")

    if not _PORT_LIST_PATTERN.fullmatch(normalized):
        raise ValidationError(
            "Ports must be a single port, a range like '1-1000', or comma-separated values/ranges."
        )

    for part in normalized.split(","):
        if "-" in part:
            start_str, end_str = part.split("-", maxsplit=1)
            start = int(start_str)
            end = int(end_str)
            if start > end:
                raise ValidationError(f"Invalid range '{part}': start cannot exceed end.")
            _assert_valid_port(start)
            _assert_valid_port(end)
            continue

        _assert_valid_port(int(part))

    return normalized


def validate_custom_args(custom_args: Sequence[str]) -> tuple[str, ...]:
    """Validate custom CLI arguments for profile 12."""
    normalized = tuple(arg.strip() for arg in custom_args if arg.strip())
    if not normalized:
        raise ValidationError("Custom scan requires at least one Nmap argument.")

    for arg in normalized:
        if "\n" in arg or "\r" in arg:
            raise ValidationError("Custom arguments cannot contain newline characters.")

    return normalized


def _assert_valid_port(port: int) -> None:
    if port < 1 or port > 65535:
        raise ValidationError(f"Port '{port}' is outside the valid range 1-65535.")
