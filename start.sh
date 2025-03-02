#!/bin/bash
# Prepare for django
python manage.py migrate
python manage.py runserver 0.0.0.0:8081
# Start uwsgi
uwsgi --ini uwsgi.ini
