#!/bin/bash

python manage.py migrate

/usr/bin/supervisord -c /etc/supervisord.conf
