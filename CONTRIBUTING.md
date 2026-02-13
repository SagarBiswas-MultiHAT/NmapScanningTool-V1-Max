# Contributing Guide

Thanks for contributing.

## Prerequisites

- Python 3.10+
- Nmap installed and available on your PATH
- Git

## Local Setup

```bash
git clone https://github.com/SagarBiswas-MultiHAT/NmapScanningTool-V2.git
cd NmapScanningTool-V2
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
# .\\.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

## Development Workflow

1. Create a feature branch from `main`.
2. Implement your changes with tests.
3. Run checks locally:

```bash
ruff check .
ruff format --check .
mypy
pytest
python -m build
```

4. Run pre-commit hooks:

```bash
pre-commit run --all-files
```

5. Open a pull request using the project PR template.

## Commit Guidelines

- Keep commits focused and atomic.
- Use clear imperative subject lines.
- Reference issues where relevant.

## Testing Expectations

- Add or update tests for behavior changes.
- Maintain at least 80% test coverage.
- Include negative and edge case tests where applicable.
