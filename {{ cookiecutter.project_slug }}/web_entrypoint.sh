#!/bin/bash

{% if cookiecutter.use_celery == 'y' %}
export CELERY_BROKER_URL="${REDIS_URL}"
{% endif %}


echo "--> Waiting for db to be ready"
./wait-for-it.sh db:5432

# Apply database migrations
echo "Apply database migrations"
python manage.py makemigration
python manage.py migrate
python manage.py collectstatic --clear --noinput
python manage.py collectstatic --noinput

# Start server
echo "--> Starting web process"
poetry run gunicorn --env DJANGO_SETTINGS_MODULE=config.settings.prod config.wsgi --bind 0.0.0.0:8000