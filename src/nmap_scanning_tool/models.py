"""Core data models used by the CLI and scanner services."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ScanProfile:
    """Represents a supported scan profile."""

    profile_id: str
    name: str
    description: str
    arguments: tuple[str, ...]
    requires_privileges: bool = False
    supports_custom_args: bool = False


@dataclass(frozen=True, slots=True)
class ScanRequest:
    """Represents a request to execute one scan."""

    target: str
    ports: str
    profile_id: str
    custom_args: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ScanResult:
    """Represents a completed scan invocation result."""

    command: tuple[str, ...]
    stdout: str
    stderr: str
    return_code: int

    @property
    def success(self) -> bool:
        """Return whether Nmap exited successfully."""
        return self.return_code == 0

    def open_port_lines(self) -> list[str]:
        """Return output lines that represent open ports in normal Nmap output."""
        lines: list[str] = []
        for line in self.stdout.splitlines():
            normalized = line.strip().lower()
            if "/" in normalized and " open " in f" {normalized} ":
                lines.append(line)
        return lines
