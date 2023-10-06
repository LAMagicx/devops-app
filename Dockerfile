FROM python:3.10

ADD . /app
WORKDIR /app
run pip install -r requirements.txt
