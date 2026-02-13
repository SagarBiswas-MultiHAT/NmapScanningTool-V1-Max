# Use a slim Python image with Nmap installed.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install --no-install-recommends -y nmap \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY src ./src
COPY main.py ./

RUN python -m pip install --upgrade pip \
    && python -m pip install .

ENTRYPOINT ["python", "main.py"]
