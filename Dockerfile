FROM python:3.10.10-slim

ENV POETRY_VERSION=1.3.2
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

ENV PATH="${PATH}:${POETRY_VENV}/bin"

RUN mkdir /climate-search-cli
WORKDIR /climate-search-cli

COPY poetry.lock /climate-search-cli
COPY pyproject.toml /climate-search-cli

RUN poetry install --no-root --no-interaction --no-ansi --without dev \
    && pip cache purge
COPY . /climate-search-cli

RUN poetry install --no-interaction --without dev

ENTRYPOINT ["poetry", "run", "cs"]