"""Command-line interface for the Nmap scanning tool."""

from __future__ import annotations

import argparse
import os
import shlex
import sys
from collections.abc import Callable, Sequence
from typing import Literal

from .config import DEFAULT_PORT_RANGE, get_default_ports
from .errors import NmapNotFoundError, NmapToolError
from .models import ScanRequest
from .profiles import list_profiles
from .scanner import NmapScanner, format_scan_output

InputFn = Callable[[str], str]
OutputFn = Callable[[str], None]
ColorName = Literal[
    "black",
    "grey",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "light_grey",
    "dark_grey",
    "light_red",
    "light_green",
    "light_yellow",
    "light_blue",
    "light_magenta",
    "light_cyan",
    "white",
]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        prog="nmap-scanner",
        description="Interactive and scriptable wrapper around Nmap common scans.",
    )
    parser.add_argument("--target", help="Target hostname or IP address.")
    parser.add_argument("--ports", help="Ports/ranges (e.g. 22,80,443 or 1-1000).")
    parser.add_argument(
        "--scan-type",
        choices=[str(index) for index in range(1, 13)],
        help="Scan profile id (1-12).",
    )
    parser.add_argument(
        "--custom-args",
        help='Custom arguments for scan type 12, e.g. "-sU --top-ports 200 -T4".',
    )
    parser.add_argument(
        "--open-only",
        action="store_true",
        help="Show only lines containing open ports.",
    )
    parser.add_argument(
        "--no-banner",
        action="store_true",
        help="Suppress startup banner output.",
    )
    return parser.parse_args(argv)


def run_cli(
    argv: Sequence[str] | None = None,
    scanner: NmapScanner | None = None,
    input_fn: InputFn = input,
    output_fn: OutputFn = print,
) -> int:
    """Execute CLI flow and return process exit code."""
    args = parse_args(argv)
    nmap_scanner = scanner or NmapScanner()

    if not args.no_banner:
        output_fn(render_banner())
        output_fn(colorize("Welcome to Nmap Scanning Tool", "cyan"))

    try:
        request = _build_request_from_args(args, input_fn=input_fn, output_fn=output_fn)
        if nmap_scanner.should_warn_for_privileges(request.profile_id):
            output_fn(
                colorize(
                    "Warning: selected scan often requires Administrator/root privileges.",
                    "yellow",
                )
            )

        nmap_scanner.ensure_nmap_available()
        result = nmap_scanner.execute(request)

        output_fn(format_scan_output(result, open_ports_only=args.open_only))
        if result.success and result.stderr:
            output_fn(colorize("Nmap warnings:", "yellow"))
            output_fn(result.stderr)
        return 0 if result.success else 1

    except (NmapToolError, ValueError) as exc:
        output_fn(colorize(f"Error: {exc}", "red"))
        if isinstance(exc, NmapNotFoundError):
            output_fn(_nmap_installation_help())
        return 1


def entrypoint() -> int:
    """Console script entrypoint."""
    return run_cli(sys.argv[1:])


def render_banner() -> str:
    """Render startup banner text, with graceful fallback when libraries are unavailable."""
    title = "Nmap Scanning Tool"
    try:
        import pyfiglet

        banner = pyfiglet.figlet_format(title)
    except Exception:
        banner = title
    return colorize(banner, "green")


def colorize(text: str, color: ColorName) -> str:
    """Colorize text when termcolor is available; otherwise return plain text."""
    try:
        from termcolor import colored

        return colored(text, color)
    except Exception:
        return text


def _build_request_from_args(
    args: argparse.Namespace,
    input_fn: InputFn,
    output_fn: OutputFn,
) -> ScanRequest:
    target = (args.target or "").strip()
    if not target:
        target = input_fn("Enter the IP address or hostname to scan: ").strip()

    default_ports = get_default_ports()
    ports = (args.ports or "").strip()
    if not ports:
        prompt = f"Enter port(s) or range (e.g., 22,80,443 or 1-1000) [default: {default_ports}]: "
        ports = input_fn(prompt).strip() or default_ports

    scan_type = (args.scan_type or "").strip()
    if not scan_type:
        output_fn("\nSelect scan type:\n")
        for profile in list_profiles():
            output_fn(f"{profile.profile_id}. {profile.name} - {profile.description}")
        scan_type = input_fn("\nEnter your choice (1-12): ").strip()

    custom_args: tuple[str, ...] = ()
    if scan_type == "12":
        raw_args = (args.custom_args or "").strip()
        if not raw_args:
            raw_args = input_fn("Enter custom Nmap arguments: ").strip()
        custom_args = tuple(shlex.split(raw_args))

    return ScanRequest(
        target=target,
        ports=ports or DEFAULT_PORT_RANGE,
        profile_id=scan_type,
        custom_args=custom_args,
    )


def _nmap_installation_help() -> str:
    if os.name == "nt":
        return (
            "Install Nmap from https://nmap.org/download.html and restart your terminal "
            "after installation."
        )
    return (
        "Install Nmap using your package manager. For example: "
        "Debian/Ubuntu: sudo apt install nmap | macOS: brew install nmap"
    )
