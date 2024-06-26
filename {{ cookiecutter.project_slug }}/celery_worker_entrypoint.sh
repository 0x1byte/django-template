#!/bin/sh

echo "--> Waiting for db to be ready"
./wait-for-it.sh postgres:5432

echo "--> Starting worker process"
poetry run celery -A config.celery_app worker -l INFO