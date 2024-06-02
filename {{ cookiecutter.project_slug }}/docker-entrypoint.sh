#!/bin/bash

echo "Applying migrations..."
poetry run python manage.py migrate

echo "Collecting static files..."
poetry run python manage.py collectstatic --no-input

echo "Starting server..."
poetry run gunicorn --env DJANGO_SETTINGS_MODULE=config.settings.prod config.wsgi --bind 0.0.0.0:8000

