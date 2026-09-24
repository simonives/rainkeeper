FROM python:3.12-slim AS app
WORKDIR /app

COPY pyproject.toml README.md ./
COPY src/ ./src/
RUN pip install --no-cache-dir . uvicorn

EXPOSE 8001
CMD ["python", "-m", "rainkeeper.http_server"]
