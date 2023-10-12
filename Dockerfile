# Use an official Python runtime as a parent image
FROM python:3.9-alpine
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
# CMD ["flask", "--host", "0.0.0.0", "--port", "5000", "--app", "app", "--debug", "run"]
