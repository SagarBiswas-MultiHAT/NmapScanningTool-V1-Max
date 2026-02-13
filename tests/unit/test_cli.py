from __future__ import annotations

from dataclasses import dataclass

from nmap_scanning_tool.cli import run_cli
from nmap_scanning_tool.errors import NmapNotFoundError
from nmap_scanning_tool.models import ScanRequest, ScanResult


@dataclass
class FakeScanner:
    result: ScanResult
    warning: bool = False
    not_found: bool = False
    captured_request: ScanRequest | None = None

    def should_warn_for_privileges(self, _profile_id: str) -> bool:
        return self.warning

    def ensure_nmap_available(self) -> str:
        if self.not_found:
            raise NmapNotFoundError("missing nmap")
        return "/usr/bin/nmap"

    def execute(self, request: ScanRequest) -> ScanResult:
        self.captured_request = request
        return self.result


def test_run_cli_non_interactive_success() -> None:
    scanner = FakeScanner(
        result=ScanResult(
            command=("nmap", "scanme.nmap.org"),
            stdout="80/tcp open http",
            stderr="",
            return_code=0,
        )
    )
    outputs: list[str] = []

    exit_code = run_cli(
        argv=["--target", "scanme.nmap.org", "--ports", "80", "--scan-type", "3", "--no-banner"],
        scanner=scanner,
        output_fn=outputs.append,
    )

    assert exit_code == 0
    assert scanner.captured_request is not None
    assert scanner.captured_request.profile_id == "3"
    assert "80/tcp open http" in outputs[-1]


def test_run_cli_interactive_custom_scan() -> None:
    scanner = FakeScanner(
        result=ScanResult(
            command=("nmap", "scanme.nmap.org"),
            stdout="done",
            stderr="",
            return_code=0,
        )
    )
    outputs: list[str] = []
    responses = iter(["scanme.nmap.org", "1-100", "12", "-sU --top-ports 100"])

    exit_code = run_cli(
        argv=["--no-banner"],
        scanner=scanner,
        input_fn=lambda _prompt: next(responses),
        output_fn=outputs.append,
    )

    assert exit_code == 0
    assert scanner.captured_request is not None
    assert scanner.captured_request.profile_id == "12"
    assert scanner.captured_request.custom_args == ("-sU", "--top-ports", "100")


def test_run_cli_handles_nmap_not_found() -> None:
    scanner = FakeScanner(
        result=ScanResult(command=("nmap",), stdout="", stderr="", return_code=0),
        not_found=True,
    )
    outputs: list[str] = []

    exit_code = run_cli(
        argv=["--target", "scanme.nmap.org", "--ports", "80", "--scan-type", "3", "--no-banner"],
        scanner=scanner,
        output_fn=outputs.append,
    )

    assert exit_code == 1
    assert any("Install Nmap" in message or "Install Nmap using" in message for message in outputs)
