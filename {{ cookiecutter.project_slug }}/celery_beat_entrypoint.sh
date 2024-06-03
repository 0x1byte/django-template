#!/bin/sh

echo "--> Waiting for db to be ready"
./wait-for-it.sh db:5432

echo "--> Starting beats process"
poetry run celery -A config.celery_app -b "${CELERY_BROKER_URL}" beat -l INFO