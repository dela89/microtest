# syntax=docker/dockerfile:1
FROM python:3-stretch
WORKDIR .
COPY . .
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 50051
CMD python greeter_server.py
