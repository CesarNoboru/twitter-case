FROM 249615491021.dkr.ecr.us-east-1.amazonaws.com/twitter-case-repo:latest

USER root
WORKDIR /app
COPY ./app/ .
RUN apk add python3 py3-pip &&\
    python3 -m pip install --upgrade python-dotenv pymysql requests urllib3 boto3

ENTRYPOINT python3 main.py
