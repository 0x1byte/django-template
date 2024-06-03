FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  
WORKDIR /app

RUN apt-get update \
  && apt-get install python3-dev default-libmysqlclient-dev gcc -y

RUN pip install --upgrade pip  
RUN pip install poetry

COPY pyproject.toml /app/

RUN poetry install

COPY . /app/

RUN chmod +x web_entrypoint.sh celery_flower_entrypoint.sh celery_worker_entrypoint.sh wait-for-it.sh celery_beat_entrypoint.sh