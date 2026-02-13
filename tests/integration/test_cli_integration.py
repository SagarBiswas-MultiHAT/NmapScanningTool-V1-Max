from __future__ import annotations

import subprocess

from nmap_scanning_tool.cli import run_cli
from nmap_scanning_tool.scanner import NmapScanner


def test_cli_with_real_scanner_components_and_fake_subprocess() -> None:
    def fake_runner(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            args=["nmap"],
            returncode=0,
            stdout="PORT    STATE SERVICE\n80/tcp  open  http\n443/tcp open  https\n",
            stderr="",
        )

    scanner = NmapScanner(runner=fake_runner, which_resolver=lambda _binary: "/usr/bin/nmap")
    outputs: list[str] = []

    exit_code = run_cli(
        argv=[
            "--target",
            "scanme.nmap.org",
            "--ports",
            "80,443",
            "--scan-type",
            "3",
            "--open-only",
            "--no-banner",
        ],
        scanner=scanner,
        output_fn=outputs.append,
    )

    assert exit_code == 0
    assert outputs[-1] == "80/tcp  open  http\n443/tcp open  https"
