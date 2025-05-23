FROM python:3.12.8

WORKDIR /app

COPY pyproject.toml ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root && \
    pip cache purge

COPY . .
