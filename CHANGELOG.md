# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-02-13

### Added

- Refactored into a production-grade `src` package layout.
- Added input validation, typed models, and custom error hierarchy.
- Added unit and integration tests with enforced coverage threshold.
- Added linting, formatting, type checking, and pre-commit automation.
- Added GitHub Actions CI workflow with lint, test, build, and dependency audit steps.
- Added Dockerfile, Makefile, Dependabot, issue templates, PR template, and editor configuration.
- Added governance and security docs: `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, and `CODE_OF_CONDUCT.md`.

### Changed

- Replaced monolithic script flow with modular CLI and scanner services.
- Updated README with complete setup, usage, testing, and project structure documentation.

### Fixed

- Eliminated inconsistent file references and outdated command examples in documentation.
- Improved open-port filtering logic to avoid false positives.

## [1.0.0] - 2025-01-01

### Added

- Initial interactive Nmap wrapper implementation.
