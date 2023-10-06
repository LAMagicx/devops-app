# Use an official Python runtime as a parent image
FROM python:3.9-alpine
ADD . /app
WORKDIR /app
run pip install -r requirements.txt
