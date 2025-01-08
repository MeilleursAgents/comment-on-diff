FROM python:3.11-slim

COPY poetry.lock pyproject.toml main.py /app/

RUN cd app && \
    apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --without dev --no-root

ENTRYPOINT ["/app/main.py"]
