#!/bin/sh

echo "--> Waiting for db to be ready"
./wait-for-it.sh postgres:5432

echo "--> Starting beats process"
poetry run celery -A config.celery_app beat -l INFO