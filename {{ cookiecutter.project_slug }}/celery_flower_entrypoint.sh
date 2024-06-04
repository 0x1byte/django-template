#!/bin/bash

echo "--> Waiting for db to be ready"
./wait-for-it.sh postgres:5432

echo "--> Starting flower process"
poetry run celery -A config.celery_app -b "${CELERY_BROKER_URL}" flower --basic_auth=${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}
