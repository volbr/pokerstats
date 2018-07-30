FROM python:3.6
MAINTAINER Volodymyr Brazhnyk <volbr@pm.me>

ARG DEVELOPMENT_MODE=true
RUN mkdir -p /app
WORKDIR /app

COPY ./requirements.txt /app
COPY ./requirements-dev.txt /app

RUN pip install -r requirements.txt
RUN [ "$DEVELOPMENT_MODE" != "true" ] || pip install -r requirements-dev.txt
ADD . /app
