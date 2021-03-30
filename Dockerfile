FROM python:3.9-alpine

WORKDIR /usr/src/app
RUN pip install -U pip && pip install slack_sdk click
COPY . .
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
