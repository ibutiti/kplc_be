ARG PYTHON_VERSION=3.10.4

FROM python:${PYTHON_VERSION}-slim

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    python3-setuptools \
    python3-wheel

RUN python -m pip install --upgrade pip
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="${PATH}:/root/.poetry/bin"
RUN poetry --version
RUN poetry config virtualenvs.create false

RUN mkdir -p /app
WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install $(test "$ENV" == production && echo "--no-dev") --no-interaction

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8080

RUN ["chmod", "+x", "/code/entrypoint.sh"]

ENTRYPOINT ["/code/entrypoint.sh"]

CMD ["help"]

# replace APP_NAME with module name
#CMD ["gunicorn", "--bind", ":8080", "--workers", "2", "kplc_outages.wsgi"]
