FROM python:3.10

SHELL ["/bin/bash", "-c"]

WORKDIR /etl/postgres_to_es

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

COPY . .

EXPOSE 8000
