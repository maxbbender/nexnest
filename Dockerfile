FROM python:3.6-alpine

RUN adduser -D nexnest

WORKDIR /home/nexnest

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY nexnest nexnest