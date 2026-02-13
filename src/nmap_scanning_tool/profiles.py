"""Definitions for built-in Nmap scan profiles."""

from __future__ import annotations

from .errors import ValidationError
from .models import ScanProfile

SCAN_PROFILES: dict[str, ScanProfile] = {
    "1": ScanProfile(
        profile_id="1",
        name="SYN Scan",
        description="Stealth SYN scan with OS detection.",
        arguments=("-sS", "-O"),
        requires_privileges=True,
    ),
    "2": ScanProfile(
        profile_id="2",
        name="Aggressive Scan",
        description="OS detection, services, scripts, and traceroute.",
        arguments=("-A",),
        requires_privileges=True,
    ),
    "3": ScanProfile(
        profile_id="3",
        name="Service Version Detection",
        description="Enumerate service versions.",
        arguments=("-sV",),
    ),
    "4": ScanProfile(
        profile_id="4",
        name="Vulnerability Scan",
        description="Run default vulnerability NSE scripts.",
        arguments=("--script=vuln",),
    ),
    "5": ScanProfile(
        profile_id="5",
        name="Heartbleed Check",
        description="Check for SSL/TLS Heartbleed vulnerability.",
        arguments=("--script=ssl-heartbleed",),
    ),
    "6": ScanProfile(
        profile_id="6",
        name="HTTP Security Headers",
        description="Inspect HTTP security headers.",
        arguments=("--script=http-security-headers",),
    ),
    "7": ScanProfile(
        profile_id="7",
        name="SQL Injection Script Check",
        description="Run HTTP SQL injection NSE script checks.",
        arguments=("--script=http-sql-injection",),
    ),
    "8": ScanProfile(
        profile_id="8",
        name="SMB Vulnerability Scan",
        description="Run SMB-focused vulnerability NSE scripts.",
        arguments=("--script=smb-vuln*",),
    ),
    "9": ScanProfile(
        profile_id="9",
        name="SSL/TLS Cipher Enumeration",
        description="List supported SSL/TLS cipher suites.",
        arguments=("--script=ssl-enum-ciphers",),
    ),
    "10": ScanProfile(
        profile_id="10",
        name="Service Discovery (Default Scripts)",
        description="Run default NSE script set.",
        arguments=("--script=default",),
    ),
    "11": ScanProfile(
        profile_id="11",
        name="OS Detection",
        description="Detect target operating system.",
        arguments=("-O",),
        requires_privileges=True,
    ),
    "12": ScanProfile(
        profile_id="12",
        name="Custom Scan",
        description="Provide custom Nmap arguments.",
        arguments=(),
        supports_custom_args=True,
    ),
}


def list_profiles() -> list[ScanProfile]:
    """Return all profiles sorted numerically by profile id."""
    return [SCAN_PROFILES[key] for key in sorted(SCAN_PROFILES, key=int)]


def get_profile(profile_id: str) -> ScanProfile:
    """Return the scan profile for the selected id."""
    try:
        return SCAN_PROFILES[profile_id]
    except KeyError as exc:
        raise ValidationError(f"Unsupported scan type '{profile_id}'.") from exc
