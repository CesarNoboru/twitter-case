FROM alpine

USER root
WORKDIR /app
COPY ./app/ .
COPY req.txt .
RUN apk add python3 py3-pip &&\
    python3 -m pip install --upgrade python-dotenv pymysql requests urllib3 boto3

ENTRYPOINT python3 main.py
