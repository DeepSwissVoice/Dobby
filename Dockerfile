FROM python:alpine

# META
LABEL maintainer="Simon (siku2)"

# EXPOSING
VOLUME /dobby/config.yml

# PREREQUISITES
RUN apk add --no-cache bash
RUN pip install pipenv 2>&1

# INSTALL
COPY Pipfile ./
COPY Pipfile.lock ./
RUN pipenv install

# SETUP
COPY dobby /dobby
COPY config.yml /dobby/_config.yml
COPY entrypoint.sh /dobby/entrypoint.sh

# RUN
ENTRYPOINT ["/dobby/entrypoint.sh"]