FROM python:latest

COPY . /nexnest
WORKDIR /nexnest

RUN pip install -r requirements.txt

CMD ["gunicorn", "-b 0.0.0.0:8080", "--log-syslog", "--reload", "manage:app"]
