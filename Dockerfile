FROM python:3.10

RUN apt-get update

RUN mkdir home/seo-optimization-cards
WORKDIR home/seo-optimization-cards

ARG POETRY_HOME=/etc/poetry
ENV PATH=${POETRY_HOME}/bin:${PATH}
RUN curl -sSL https://install.python-poetry.org | python -
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-cache --without additional && poetry cache clear pypi --all

COPY . ./

CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "api.main:app"]