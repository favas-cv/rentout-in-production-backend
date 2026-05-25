#!/bin/sh

echo "Waiting for PostgreSQL..."

while ! nc -z postgres 5432; do
  sleep 1
done

echo "PostgreSQL Started"

python manage.py migrate --noinput

python manage.py collectstatic --noinput

exec daphne -b 0.0.0.0 -p 8000 config.asgi:application