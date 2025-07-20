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

HEALTHCHECK --interval=2m --timeout=3s --start-period=5s --retries=3 \
    CMD python3 -c "import http.client; conn = http.client.HTTPConnection('localhost', 8081); conn.request('GET', '/health'); res = conn.getresponse(); exit(0) if res.status == 200 else exit(1)"

EXPOSE 8081

CMD ["gunicorn", "-b", "0.0.0.0:8081", "app:create_app()"]