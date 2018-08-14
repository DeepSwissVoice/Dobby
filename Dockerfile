FROM python:alpine

# META
LABEL maintainer="Simon (siku2)"

# PREREQUISITES
RUN pip install pipenv
RUN pip install https://github.com/Supervisor/supervisor/archive/master.zip

WORKDIR /dobby

# INSTALL
COPY Pipfile ./
COPY Pipfile.lock ./
RUN pipenv sync

# SETUP
COPY dobby dobby
COPY ext ext
COPY config.yml ./_config.yml
COPY .docker/entrypoint.sh ./
COPY .docker/supervisord.conf /etc/

RUN chmod +x entrypoint.sh

# RUN
ENTRYPOINT ["./entrypoint.sh"]