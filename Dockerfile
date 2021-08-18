# syntax=docker/dockerfile:1
FROM python:3-stretch
WORKDIR /code
#ENV FLASK_APP=./web_display/app.py
#ENV FLASK_RUN_HOST=0.0.0.0
#COPY requirements.txt requirements.txt
#RUN pip install -r requirements.txt
#EXPOSE 5000
COPY . .
CMD ["python", "greeter_client.py"]
