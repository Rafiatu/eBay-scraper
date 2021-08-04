FROM python:3.9.6-alpine as base

COPY src/scraper /scraper

WORKDIR /scraper

COPY ./requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT["python"]
