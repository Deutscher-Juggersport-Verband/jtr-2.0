#!/bin/sh

echo "Waiting for MySQL to start"
while ! nc -z mysql 3306; do
  sleep 1
done
echo "MySQL started"

exec gunicorn \
  --certfile="${SSL_CERT_PATH}" \
  --keyfile="${SSL_KEY_PATH}" \
  -w 10 \
  -b 0.0.0.0:8080 wsgi:app
