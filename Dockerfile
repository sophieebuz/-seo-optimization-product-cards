FROM python:3.10-slim

RUN apt-get update && apt-get -y install curl

RUN mkdir home/seo-optimization-cards
WORKDIR home/seo-optimization-cards

ARG POETRY_HOME=/etc/poetry
ENV PATH=${POETRY_HOME}/bin:${PATH}
RUN curl -sSL https://install.python-poetry.org | python -
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-cache --without additional && poetry cache clear pypi --all

COPY . ./

CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "api.main:app"]