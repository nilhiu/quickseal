FROM astral/uv:python3.13-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Use system interpreter
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

FROM  python:3.13-alpine

WORKDIR /app

COPY --from=builder --chown=app-user:app-user /app .

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8081

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "8081", "--no-debug"]