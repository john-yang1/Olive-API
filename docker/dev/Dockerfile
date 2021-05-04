FROM python:3.7

LABEL maintainer="Dan Harrison dan@olive.app"

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1

EXPOSE 80

COPY . /code/
WORKDIR /code/

RUN pip install -r /code/requirements/dev.txt

COPY ./docker/dev/start.sh /tmp/start.sh

RUN chmod +x /tmp/start.sh

RUN mkdir /var/log/app

CMD ["/tmp/start.sh"]
