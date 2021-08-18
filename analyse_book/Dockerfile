# syntax=docker/dockerfile:1
FROM python:3-stretch
WORKDIR .
COPY . .
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD ./wait-for-it.sh greeter_server:50051 -- python greeter_client.py
