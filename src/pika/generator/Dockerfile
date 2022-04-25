FROM python:3.11.0a7-alpine3.15

ENV PYTHONUNBUFFERED 1

RUN python -m pip install pika --upgrade
RUN mkdir -p /opt/generator
WORKDIR /opt/generator

RUN apk add hunspell-en