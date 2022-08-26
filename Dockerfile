ARG PYTHON_VERSION=3.10.6-slim

FROM python:${PYTHON_VERSION} as build

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    curl \
    libpq-dev

RUN python -m pip install --upgrade pip

ENV POETRY_VERSION 1.1.15
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN python -m venv --copies /opt/venv

RUN . /opt/venv/bin/activate && poetry install --no-dev


FROM python:${PYTHON_VERSION} as prod

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update &&  \
    apt-get install -y --no-install-recommends libpq-dev &&  \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=build /opt/venv /opt/venv/
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY . ./

EXPOSE 8000

RUN ["chmod", "+x", "/app/entrypoint.sh"]

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["gunicorn"]
