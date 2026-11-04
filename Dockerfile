FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

FROM base AS web
COPY src/ ./src/
USER 10001:10001
EXPOSE 8080
CMD ["python", "-m", "http.server", "8080", "--bind", "0.0.0.0", "--directory", "/app/src"]

FROM base AS tests
RUN apt-get update \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-dev.txt ./
RUN python -m pip install --no-cache-dir -r requirements-dev.txt

COPY pytest.ini ./
COPY src/ ./src/
COPY tests/ ./tests/

CMD ["sh", "-c", "python --version && node --version && python -m pytest -v -p no:cacheprovider && node tests/api.tests.js"]
