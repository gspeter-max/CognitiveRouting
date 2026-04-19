FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml ./
COPY src ./src

RUN uv sync --no-dev

CMD ["python", "-m", "cognitive_routing.demo_phase1"]

