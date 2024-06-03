#!/bin/sh

echo "--> Waiting for db to be ready"
./wait-for-it.sh db:5432

echo "--> Starting worker process"
poetry run celery -A config.celery_app -b "${CELERY_BROKER_URL}" worker -l INFO