FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PATH="/app/.venv/bin:${PATH}" \
    PYTHONPATH="/app/src"

WORKDIR /app

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    curl git build-essential \
    libglib2.0-0 libnss3 libatk-bridge2.0-0 libx11-xcb1 libxcomposite1 libxdamage1 libxfixes3 \
    libxrandr2 libgbm1 libgtk-3-0 libpango-1.0-0 libcairo2 libcups2 libdrm2 libasound2 \
    libxkbcommon0 libxshmfence1 libxss1 libxcursor1 libxi6 libxtst6 libxrender1 fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv==0.4.22 && \
    uv sync --frozen --no-dev --python /usr/local/bin/python

RUN python -m playwright install --with-deps chromium

COPY . .

EXPOSE 8888 4040
CMD ["sh", "-c", "\
  uv run jupyter lab \
    --ip=0.0.0.0 --port=8888 --allow-root \
    --ServerApp.token='' \
    --ServerApp.password='' \
    --ServerApp.disable_check_xsrf=True \
    --ServerApp.allow_remote_access=True \
  & \
  echo 'Waiting for Jupyter to be ready...'; \
  until curl -sSf http://127.0.0.1:8888/lab >/dev/null 2>&1; do \
    echo 'Still waiting for Jupyter...'; \
    sleep 2; \
  done; \
  echo 'Jupyter is up, starting MCP server...'; \
  uv run jupyter-mcp-server start \
    --transport streamable-http \
    --jupyter-url http://127.0.0.1:8888 \
    --port 4040 \
  & \
  uv run python -m src.worker.sqs_worker \
  "]
