FROM python:3.10-slim

RUN apt-get update && apt-get -y install curl

RUN mkdir home/seo-optimization-cards
WORKDIR home/seo-optimization-cards

ARG POETRY_HOME=/etc/poetry
ENV PATH=${POETRY_HOME}/bin:${PATH}
RUN curl -sSL https://install.python-poetry.org | python -
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-cache --only pgjob && poetry cache clear pypi --all

COPY data/data/ ./data/data/
COPY k8s/pgjob/ ./k8s/pgjob/
