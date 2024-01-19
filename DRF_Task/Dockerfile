FROM python:3.11-slim-bullseye
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y postgresql-client libjpeg-dev libpq-dev gcc
RUN  pip install -r requirements.txt
COPY . .