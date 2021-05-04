FROM python:3.7

LABEL maintainer="Dan Harrison dan@olive.app"

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1

EXPOSE 80

COPY . /code/
WORKDIR /code/

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r /code/requirements/prod.txt

COPY ./docker/supervisord.conf /etc/supervisord.conf
COPY ./docker/nginx.conf /etc/nginx/nginx.conf
COPY ./docker/uwsgi.ini /etc/uwsgi/uwsgi.ini

COPY ./docker/stage/start.sh /tmp/start.sh

RUN chmod +x /tmp/start.sh

RUN mkdir /var/log/app

CMD ["/tmp/start.sh"]
