"""Nmap scanner service orchestration."""

from __future__ import annotations

import os
import subprocess
from collections.abc import Callable

from .config import DEFAULT_PORT_RANGE, get_nmap_binary
from .errors import NmapNotFoundError, ScanExecutionError
from .models import ScanRequest, ScanResult
from .profiles import get_profile
from .validation import validate_custom_args, validate_ports, validate_target

CompletedProcessRunner = Callable[..., subprocess.CompletedProcess[str]]
WhichResolver = Callable[[str], str | None]


class NmapScanner:
    """Build and execute Nmap scan commands."""

    def __init__(
        self,
        nmap_binary: str | None = None,
        runner: CompletedProcessRunner = subprocess.run,
        which_resolver: WhichResolver | None = None,
    ) -> None:
        self._nmap_binary = nmap_binary or get_nmap_binary()
        self._runner = runner
        self._which_resolver = which_resolver or _default_which

    @property
    def nmap_binary(self) -> str:
        """Return configured Nmap binary."""
        return self._nmap_binary

    def ensure_nmap_available(self) -> str:
        """Return discovered Nmap path or raise if it is unavailable."""
        path = self._which_resolver(self._nmap_binary)
        if path is None:
            raise NmapNotFoundError(f"Nmap executable '{self._nmap_binary}' was not found in PATH.")
        return path

    def should_warn_for_privileges(self, profile_id: str) -> bool:
        """Return True when selected profile usually needs elevation and process is not elevated."""
        profile = get_profile(profile_id)
        if not profile.requires_privileges:
            return False

        is_elevated = _is_elevated_process()
        return is_elevated is False

    def build_command(self, request: ScanRequest) -> tuple[str, ...]:
        """Construct an Nmap command for a validated scan request."""
        target = validate_target(request.target)
        ports = validate_ports(request.ports or DEFAULT_PORT_RANGE)
        profile = get_profile(request.profile_id)

        args: tuple[str, ...]
        include_ports = True
        if profile.supports_custom_args:
            args = validate_custom_args(request.custom_args)
            include_ports = not _contains_port_flag(args)
        else:
            args = profile.arguments

        command: list[str] = [self._nmap_binary, target]
        if include_ports:
            command.extend(["-p", ports])
        command.extend(args)
        return tuple(command)

    def execute(self, request: ScanRequest) -> ScanResult:
        """Execute one scan request and return the command result."""
        command = self.build_command(request)

        try:
            completed = self._runner(
                list(command),
                capture_output=True,
                text=True,
                check=False,
            )
        except FileNotFoundError as exc:
            raise NmapNotFoundError(
                f"Unable to execute '{self._nmap_binary}'. "
                "Confirm installation and PATH configuration."
            ) from exc
        except OSError as exc:
            raise ScanExecutionError(f"Failed to start scan process: {exc}") from exc

        return ScanResult(
            command=command,
            stdout=completed.stdout.strip(),
            stderr=completed.stderr.strip(),
            return_code=completed.returncode,
        )


def format_scan_output(result: ScanResult, open_ports_only: bool) -> str:
    """Render scan output according to user-selected display mode."""
    if not result.success:
        detail = result.stderr or "No additional error information was provided by Nmap."
        return f"Nmap exited with code {result.return_code}.\n{detail}"

    if open_ports_only:
        lines = result.open_port_lines()
        if lines:
            return "\n".join(lines)
        return "No open ports reported by Nmap for the selected target and scan."

    return result.stdout or "Nmap did not return any output."


def _default_which(binary: str) -> str | None:
    import shutil

    return shutil.which(binary)


def _is_elevated_process() -> bool | None:
    if os.name == "nt":
        try:
            import ctypes

            windll = getattr(ctypes, "windll", None)
            if windll is None:
                return None

            shell32 = getattr(windll, "shell32", None)
            if shell32 is None:
                return None

            is_user_an_admin = getattr(shell32, "IsUserAnAdmin", None)
            if callable(is_user_an_admin):
                return bool(is_user_an_admin())
            return None
        except Exception:
            return None

    geteuid = getattr(os, "geteuid", None)
    if callable(geteuid):
        uid = int(geteuid())
        return uid == 0

    return None


def contains_port_override(args: tuple[str, ...] | list[str]) -> bool:
    """Expose port-flag detection for tests and callers."""
    return _contains_port_flag(args)


def _contains_port_flag(args: tuple[str, ...] | list[str]) -> bool:
    for arg in args:
        if arg in {"-p", "--ports"}:
            return True
        if arg.startswith("-p") and arg != "-Pn":
            return True
        if arg.startswith("--ports="):
            return True
    return False
