from __future__ import annotations

import pytest

from nmap_scanning_tool.errors import ValidationError
from nmap_scanning_tool.validation import validate_custom_args, validate_ports, validate_target


@pytest.mark.parametrize("target", ["127.0.0.1", "::1", "scanme.nmap.org", "example-host.local"])
def test_validate_target_accepts_valid_values(target: str) -> None:
    assert validate_target(target) == target


@pytest.mark.parametrize("target", ["", "bad target", "%%%", "-host.example"])
def test_validate_target_rejects_invalid_values(target: str) -> None:
    with pytest.raises(ValidationError):
        validate_target(target)


@pytest.mark.parametrize(
    "ports",
    [
        "1",
        "443",
        "1-1024",
        "22,80,443",
        "1-10,443,8080-8090",
    ],
)
def test_validate_ports_accepts_valid_values(ports: str) -> None:
    assert validate_ports(ports) == ports


@pytest.mark.parametrize("ports", ["0", "65536", "100-1", "abc", "22,,80", "1-70000"])
def test_validate_ports_rejects_invalid_values(ports: str) -> None:
    with pytest.raises(ValidationError):
        validate_ports(ports)


def test_validate_custom_args_requires_values() -> None:
    with pytest.raises(ValidationError):
        validate_custom_args(())


def test_validate_custom_args_strips_blanks() -> None:
    assert validate_custom_args(["-sU", "   ", "--top-ports", "200"]) == (
        "-sU",
        "--top-ports",
        "200",
    )
