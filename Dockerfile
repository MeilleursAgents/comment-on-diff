FROM python:3.8

COPY . /app
WORKDIR /app

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

ENTRYPOINT ["./main.py"]
