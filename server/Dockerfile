FROM python:3.6
MAINTAINER Volodymyr Brazhnyk <volbr@pm.me>

RUN mkdir -p /app
WORKDIR /app

ADD requirements.txt /app
ADD dev-requirements.txt /app
RUN pip install -r requirements.txt
RUN pip install -r dev-requirements.txt
ADD . /app
