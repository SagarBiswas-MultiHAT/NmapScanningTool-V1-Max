# Nmap Scanning Tool

A secure, production-ready CLI wrapper that makes common Nmap scan workflows faster, safer, and easier to run.

<div align="right">

[![CI](https://github.com/SagarBiswas-MultiHAT/NmapScanningTool-V1-Max/actions/workflows/ci.yml/badge.svg)](https://github.com/SagarBiswas-MultiHAT/NmapScanningTool-V1-Max/actions/workflows/ci.yml)
&nbsp;
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
&nbsp;
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
&nbsp;
[![Version](https://img.shields.io/badge/version-2.0.0-brightgreen.svg)](CHANGELOG.md)

</div>

## What This Project Is

This project is an interactive and scriptable front-end for Nmap. It helps security engineers, sysadmins, and students run common scans consistently without memorizing long command combinations. You can use preset scan profiles, run custom arguments, and optionally filter output to open ports only. It also adds guardrails like input validation, privilege warnings, and clear error messages.

## Features

- 12 built-in scan profiles, including SYN, aggressive, OS detection, and vulnerability-focused NSE scans
- Custom scan mode for advanced Nmap users
- Interactive prompts for beginner-friendly execution
- Non-interactive flags for scripting and automation
- Strict validation for targets, ports, and custom arguments
- Typed, modular Python architecture with testable services
- CI pipeline with lint, type-check, tests, build, and dependency audit
- Docker support for reproducible runtime setup

## Testing: 

<b>Terminal 1</b>

```
┏━(Message from Kali developers)
┃
┃ This is a minimal installation of Kali Linux, you likely
┃ want to install supplementary tools. Learn how:
┃ ⇒ https://www.kali.org/docs/troubleshooting/common-minimum-setup/
┃
┗━(Run: “touch ~/.hushlogin” to hide this message)
┌──(BlackHAT㉿HP-SAGAR)-[/mnt/h/updatedReposV2/NmapScanningTool-V1-Max]
└─$ python3 -m http.server 8000
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

When testing OS detection locally, a simple HTTP server was started using python3 -m http.server 8000. This creates a temporary web service listening on port 8000 (0.0.0.0:8000), allowing Nmap to detect at least one open port. OS fingerprinting requires both open and closed ports to accurately analyze TCP/IP behavior. Without an active service, all ports appear closed and OS detection becomes unreliable. Running this lightweight server ensures realistic scan results and validates that the Nmap Scanning Tool correctly performs port discovery and operating system detection.

<b>Terminal 2</b>

```
┌──(.venv)(BlackHAT㉿HP-SAGAR)-[/mnt/h/updatedReposV2/NmapScanningTool-V1-Max]
└─$ python main.py
 _   _                         ____                        _
| \ | |_ __ ___   __ _ _ __   / ___|  ___ __ _ _ __  _ __ (_)_ __   __ _ 
|  \| | '_ ` _ \ / _` | '_ \  \___ \ / __/ _` | '_ \| '_ \| | '_ \ / _` |
| |\  | | | | | | (_| | |_) |  ___) | (_| (_| | | | | | | | | | | | (_| |
|_| \_|_| |_| |_|\__,_| .__/  |____/ \___\__,_|_| |_|_| |_|_|_| |_|\__, |
                      |_|                                          |___/ 
 _____           _ 
|_   _|__   ___ | |
  | |/ _ \ / _ \| |
  | | (_) | (_) | |
  |_|\___/ \___/|_|


Welcome to Nmap Scanning Tool
Enter the IP address or hostname to scan: 127.0.0.1
Enter port(s) or range (e.g., 22,80,443 or 1-1000) [default: 1-65535]: 

Select scan type:

1. SYN Scan - Stealth SYN scan with OS detection.
2. Aggressive Scan - OS detection, services, scripts, and traceroute.
3. Service Version Detection - Enumerate service versions.
4. Vulnerability Scan - Run default vulnerability NSE scripts.
5. Heartbleed Check - Check for SSL/TLS Heartbleed vulnerability.
6. HTTP Security Headers - Inspect HTTP security headers.
7. SQL Injection Script Check - Run HTTP SQL injection NSE script checks.
8. SMB Vulnerability Scan - Run SMB-focused vulnerability NSE scripts.
9. SSL/TLS Cipher Enumeration - List supported SSL/TLS cipher suites.
10. Service Discovery (Default Scripts) - Run default NSE script set.
11. OS Detection - Detect target operating system.
12. Custom Scan - Provide custom Nmap arguments.

Enter your choice (1-12): 11
Warning: selected scan often requires Administrator/root privileges.
Starting Nmap 7.95 ( https://nmap.org ) at 2026-02-14 00:44 +06
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000084s latency).
Not shown: 65534 closed tcp ports (reset)
PORT     STATE SERVICE
8000/tcp open  http-alt
Device type: general purpose
Running: Linux 2.6.X|5.X
OS CPE: cpe:/o:linux:linux_kernel:2.6.32 cpe:/o:linux:linux_kernel:5 cpe:/o:linux:linux_kernel:6
OS details: Linux 2.6.32, Linux 5.0 - 6.2
Network Distance: 0 hops

OS detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 2.33 seconds
```




## Quick Start

### Prerequisites

- Python 3.10 or newer
- Nmap installed and available in your PATH
  - Windows: https://nmap.org/download
  - Debian/Ubuntu: `sudo apt install nmap`
  - macOS (Homebrew): `brew install nmap`

### Installation

```bash
git clone https://github.com/SagarBiswas-MultiHAT/NmapScanningTool-V1-Max.git
cd NmapScanningTool-V1-Max
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
# .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

### Run The Project

```bash
python main.py
```

You should see a banner, a target prompt, a port prompt, and the scan profile menu.

## Usage Examples

### 1) Interactive mode

```bash
python main.py
```

What it does: walks you through target, ports, scan type, and output filtering.

### 2) Non-interactive profile scan

```bash
python main.py --target scanme.nmap.org --ports 80,443 --scan-type 3 --open-only
```

What it does: runs service version detection (`-sV`) and prints only open-port lines.

### 3) Custom scan arguments

```bash
python main.py --target scanme.nmap.org --ports 1-1000 --scan-type 12 --custom-args "-sU --top-ports 100 -T4"
```

What it does: runs a custom UDP-focused scan with your supplied flags.

## CLI Reference

### Command-line options

| Flag | Description | Interactive behaviour | Notes |
| --- | --- | --- | --- |
| `--target` | hostname or IP address to scan | Prompts `Enter the IP address or hostname to scan:` if omitted. | Accepts IP v4, IPv6, or DNS names; trims whitespace. |
| `--ports` | ports or ranges (`22,80,443`, `1-1000`, etc.) | Prompts `Enter port(s) or range (e.g., 22,80,443 or 1-1000) [default: 1-65535]:` when missing and falls back to `NMAP_DEFAULT_PORTS` env value (`1-65535` otherwise). | Supports comma-separated lists and hyphenated ranges. |
| `--scan-type` | selects one of the 12 built-in profiles | Displays the numbered list of profiles via `Select scan type:` and prompts `Enter your choice (1-12):` when not provided. | Only values `1` through `12` are accepted; invalid choices raise an error. |
| `--custom-args` | custom Nmap arguments parsed with `shlex.split()` | If `--scan-type 12` (Custom Scan), prompts `Enter custom Nmap arguments:` when the flag is omitted. | Arguments are passed directly to `nmap` in addition to the default command line. |
| `--open-only` | filter output to lines containing open ports | Not applicable in interactive prompt. | Equivalent to `--open-only` flag in CLI runs. |
| `--no-banner` | suppress the ASCII banner | Not applicable in interactive prompt. | Useful for scripting and quiet CI runs. |

### Interactive prompts and defaults

- **Target prompt:** `Enter the IP address or hostname to scan:` – required when `--target` is absent.
- **Ports prompt:** `Enter port(s) or range (e.g., 22,80,443 or 1-1000) [default: 1-65535]` – uses `NMAP_DEFAULT_PORTS` (default `1-65535`) if left blank.
- **Scan type prompt:** prints the entire profile list, then `Enter your choice (1-12):` to pick one (see profiles below).
- **Custom args prompt:** `Enter custom Nmap arguments:` only when profile `12` is selected and neither `--custom-args` nor automatic values are provided.
- **Warnings:** Certain profiles (1, 2, and 11) emit a privilege warning (`Warning: selected scan often requires Administrator/root privileges.`).
- **Environment overrides:** `NMAP_BINARY` and `NMAP_DEFAULT_PORTS` allow customizing which `nmap` binary runs and what default port range is offered during prompts or when `--ports` is missing.

### Scan profiles (select via `--scan-type` or interactive menu)

| ID | Name | Description | Default Nmap arguments | Requires privileges |
| --- | --- | --- | --- | --- |
| 1 | SYN Scan | Stealth SYN scan with OS detection. | `-sS -O` | Yes |
| 2 | Aggressive Scan | OS detection, services, scripts, traceroute. | `-A` | Yes |
| 3 | Service Version Detection | Enumerate service versions. | `-sV` | No |
| 4 | Vulnerability Scan | Run default vulnerability NSE scripts. | `--script=vuln` | No |
| 5 | Heartbleed Check | Check for SSL/TLS Heartbleed vulnerability. | `--script=ssl-heartbleed` | No |
| 6 | HTTP Security Headers | Inspect HTTP security headers. | `--script=http-security-headers` | No |
| 7 | SQL Injection Script Check | Run HTTP SQL injection NSE script checks. | `--script=http-sql-injection` | No |
| 8 | SMB Vulnerability Scan | Run SMB-focused vulnerability NSE scripts. | `--script=smb-vuln*` | No |
| 9 | SSL/TLS Cipher Enumeration | List supported SSL/TLS cipher suites. | `--script=ssl-enum-ciphers` | No |
| 10 | Service Discovery | Run default NSE script set. | `--script=default` | No |
| 11 | OS Detection | Detect target operating system. | `-O` | Yes |
| 12 | Custom Scan | Provide custom Nmap arguments. | none | Depends on args |

## Input Examples

1. **Fully interactive run:**

  ```bash
  python main.py
  # Prompts target, ports, scan type menu, and custom args when needed.
  ```

2. **Non-interactive service-version scan showing only open ports:**

  ```bash
  python main.py --target scanme.nmap.org --ports 80,443 --scan-type 3 --open-only
  ```

3. **Custom scan with UDP focus using inline arguments:**

  ```bash
  python main.py --target 192.0.2.1 --scan-type 12 --custom-args "-sU --top-ports 100 -T4" --no-banner
  ```

4. **Default-port scan using environment override:**

  ```bash
  set NMAP_DEFAULT_PORTS=20-1024 && python main.py --target 10.0.0.5 --scan-type 11
  ```

5. **Interactive custom scan fallback:**

  ```bash
  python main.py --target example.com --scan-type 12
  # When --custom-args missing, CLI asks: Enter custom Nmap arguments:
  # e.g. -sS --script=ssl-heartbleed -p 443
  ```

## Project Structure

```text
NmapScanningTool-V1-Max/
|-- .github/
|   |-- workflows/ci.yml              # Lint, test, build, dependency audit
|   |-- ISSUE_TEMPLATE/               # Bug and feature request templates
|   |-- PULL_REQUEST_TEMPLATE.md      # Pull request checklist
|   `-- dependabot.yml                # Automated dependency updates
|-- src/nmap_scanning_tool/
|   |-- cli.py                        # CLI parsing, prompts, user interaction
|   |-- scanner.py                    # Command construction and subprocess execution
|   |-- validation.py                 # Target/port/custom-arg validation
|   |-- profiles.py                   # Built-in scan profile definitions
|   |-- models.py                     # Typed request/result/profile models
|   |-- errors.py                     # Custom exception hierarchy
|   `-- config.py                     # Environment-driven configuration helpers
|-- tests/
|   |-- unit/                         # Unit tests for each module
|   `-- integration/                  # End-to-end CLI flow with mocked subprocess
|-- main.py                           # Backward-compatible local launcher
|-- pyproject.toml                    # Packaging and toolchain config
|-- Makefile                          # Common developer commands
|-- Dockerfile                        # Container runtime with Nmap installed
`-- README.md                         # Project documentation
```

## Running Tests

```bash
python -m pytest
```

Coverage is enforced at 80%+ via `pyproject.toml`. To inspect coverage output explicitly:

```bash
python -m pytest --cov=src/nmap_scanning_tool --cov-report=term-missing
```

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) for setup, quality gates, and pull request standards.

## Roadmap

- [ ] Add optional JSON output mode for machine-readable integrations
- [ ] Add profile presets for common compliance checks
- [ ] Add optional scan result export (.txt, .xml, .json)
- [ ] Add richer terminal UI mode with progress indicators
- [ ] Add signed release artifacts

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- [Nmap](https://nmap.org/) for the scanning engine
- [pyfiglet](https://pypi.org/project/pyfiglet/) for banner rendering
- [termcolor](https://pypi.org/project/termcolor/) for terminal color output
