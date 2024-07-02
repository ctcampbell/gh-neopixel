FROM python:3.12-alpine3.19 AS builder

WORKDIR /app

RUN apk add --no-cache curl build-base libffi-dev openssl-dev cargo && \
curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/root/.local/bin" PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
RUN python -m venv /venv

COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt | /venv/bin/pip install -r /dev/stdin

COPY . .
RUN poetry build && /venv/bin/pip install dist/*.whl

FROM python:3.12-slim
COPY --from=builder /venv /venv
ENTRYPOINT ["/venv/bin/python", "-m", "ghneopixel"]