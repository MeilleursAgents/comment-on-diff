FROM python:3.8

ADD main.py /main.py

ENTRYPOINT ["./main.py"]
