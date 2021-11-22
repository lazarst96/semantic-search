FROM python:3.8-alpine
MAINTAINER Lazar Stamenkovic

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
COPY ./requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip

RUN apk add --update --no-cache musl-dev linux-headers g++
RUN pip install -r /app/requirements.txt

RUN python -m spacy download en_core_web_sm

WORKDIR /app
COPY ./src /app/src
COPY ./start.sh /app/start.sh


RUN chmod +x ./start.sh
RUN adduser -D user
USER user