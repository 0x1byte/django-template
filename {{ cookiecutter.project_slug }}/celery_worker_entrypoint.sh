#!/bin/sh

echo "--> Waiting for db to be ready"
./wait-for-it.sh db:5432

echo "--> Starting worker process"
celery -A config.celery_app worker -l INFO