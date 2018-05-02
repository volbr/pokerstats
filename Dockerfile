FROM python:3.6
MAINTAINER volbr

RUN mkdir -p /app
WORKDIR /app

ADD requirements.txt /app
RUN pip install -r requirements.txt
ADD . /app
