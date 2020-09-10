FROM python:3.8-slim

COPY . /app
WORKDIR /app

RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

ENTRYPOINT ["/app/main.py"]
