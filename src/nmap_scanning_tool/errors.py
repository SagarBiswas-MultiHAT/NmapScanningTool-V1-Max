"""Custom exceptions for the Nmap scanning tool."""


class NmapToolError(Exception):
    """Base exception type for all application-level errors."""


class ValidationError(NmapToolError):
    """Raised when user-provided input fails validation."""


class NmapNotFoundError(NmapToolError):
    """Raised when the Nmap binary cannot be discovered."""


class ScanExecutionError(NmapToolError):
    """Raised when an Nmap scan command returns an error."""
