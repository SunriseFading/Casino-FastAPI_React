FROM python:3.11-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -
ENV PATH=$PATH:/etc/poetry/bin

COPY ./pyproject.toml ./poetry.lock ./
RUN poetry config virtualenvs.in-project true
RUN poetry install --only main
RUN poetry add uvloop

FROM python:3.11-slim
ENV PATH=/app/.venv/bin:$PATH \
    PYTHONPATH=$PYTHONPATH:/app
WORKDIR /app
COPY src src
COPY --from=builder /app/.venv .venv
ENTRYPOINT ["sh", "-c", "uvicorn src.main:create_app --host 0.0.0.0 --port 8000"]
