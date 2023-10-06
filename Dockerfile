FROM python:3.11

ADD . /app
WORKDIR /app
run pip install -r requirements.txt
