from __future__ import annotations

import subprocess

import pytest

from nmap_scanning_tool.errors import NmapNotFoundError
from nmap_scanning_tool.models import ScanRequest, ScanResult
from nmap_scanning_tool.scanner import NmapScanner, contains_port_override, format_scan_output


def test_ensure_nmap_available_returns_resolved_path() -> None:
    scanner = NmapScanner(which_resolver=lambda _binary: "/usr/bin/nmap")
    assert scanner.ensure_nmap_available() == "/usr/bin/nmap"


def test_ensure_nmap_available_raises_when_missing() -> None:
    scanner = NmapScanner(which_resolver=lambda _binary: None)
    with pytest.raises(NmapNotFoundError):
        scanner.ensure_nmap_available()


def test_build_command_with_standard_profile() -> None:
    scanner = NmapScanner(which_resolver=lambda _binary: "/usr/bin/nmap")
    request = ScanRequest(target="scanme.nmap.org", ports="80,443", profile_id="3")
    command = scanner.build_command(request)

    assert command == ("nmap", "scanme.nmap.org", "-p", "80,443", "-sV")


def test_build_command_custom_profile_respects_port_override() -> None:
    scanner = NmapScanner(which_resolver=lambda _binary: "/usr/bin/nmap")
    request = ScanRequest(
        target="scanme.nmap.org",
        ports="1-1000",
        profile_id="12",
        custom_args=("-sU", "--ports", "53,67,68"),
    )
    command = scanner.build_command(request)

    assert command == ("nmap", "scanme.nmap.org", "-sU", "--ports", "53,67,68")


def test_execute_returns_scan_result() -> None:
    def fake_runner(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            args=["nmap"],
            returncode=0,
            stdout="80/tcp open http\n",
            stderr="",
        )

    scanner = NmapScanner(runner=fake_runner, which_resolver=lambda _binary: "/usr/bin/nmap")
    result = scanner.execute(ScanRequest(target="scanme.nmap.org", ports="80", profile_id="3"))

    assert result.success is True
    assert result.stdout == "80/tcp open http"


def test_format_scan_output_handles_open_only_filter() -> None:
    result = ScanResult(
        command=("nmap", "example.com"),
        stdout="80/tcp open http\n443/tcp open https\n8080/tcp closed http-proxy",
        stderr="",
        return_code=0,
    )

    rendered = format_scan_output(result, open_ports_only=True)
    assert rendered == "80/tcp open http\n443/tcp open https"


def test_contains_port_override_detects_variants() -> None:
    assert contains_port_override(("--ports", "80")) is True
    assert contains_port_override(("-p22", "-sV")) is True
    assert contains_port_override(("--ports=53,67",)) is True
    assert contains_port_override(("-sV", "-Pn")) is False
