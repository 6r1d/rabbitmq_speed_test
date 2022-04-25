FROM python:3.11.0a7-bullseye

ENV PYTHONUNBUFFERED 1
# https://github.com/aio-libs/aiohttp/issues/6600
ENV AIOHTTP_NO_EXTENSIONS = 1
# https://github.com/aio-libs/yarl/issues/680
ENV YARL_NO_EXTENSIONS = 1

RUN apt-get update && apt-get install -y python3-dev

RUN python -m pip install aio-pika --upgrade
RUN mkdir -p /opt/receiver
WORKDIR /opt/receiver