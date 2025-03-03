#!/bin/bash
# Prepare for django
python manage.py makemigrations
python manage.py migrate
# Start uwsgi
uwsgi --ini uwsgi.ini
