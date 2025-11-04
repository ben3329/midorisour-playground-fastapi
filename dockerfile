# syntax=docker/dockerfile:1.4
FROM python:3.13

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml /app/

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --only main --no-interaction --no-ansi

COPY app /app/app

EXPOSE 8000

CMD [ "fastapi", "run" ]