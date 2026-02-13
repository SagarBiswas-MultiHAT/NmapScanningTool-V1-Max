.PHONY: install install-dev lint format typecheck test test-cov build audit run clean

install:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt

install-dev:
	python -m pip install --upgrade pip
	python -m pip install -e .[dev]

lint:
	ruff check .

format:
	ruff format .

format-check:
	ruff format --check .

typecheck:
	mypy

test:
	pytest

test-cov:
	pytest --cov=src/nmap_scanning_tool --cov-report=term-missing --cov-fail-under=80

build:
	python -m build

audit:
	pip-audit --requirement requirements.txt --progress-spinner off

run:
	python main.py

clean:
	python -c "import glob, pathlib, shutil; [shutil.rmtree(p, ignore_errors=True) for p in ['.pytest_cache', '.ruff_cache', '.mypy_cache', 'htmlcov', 'dist', 'build'] + glob.glob('*.egg-info')]; [pathlib.Path(p).unlink(missing_ok=True) for p in glob.glob('.coverage*')]"
