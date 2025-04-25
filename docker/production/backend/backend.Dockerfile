FROM python:3.13-alpine

RUN apk add --no-cache  \
    g++ \
    linux-headers

WORKDIR /app

COPY ../../../backend .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /opt/scripts

COPY docker/production/backend/entrypoint.sh /opt/scripts/entrypoint.sh

RUN chmod +x /opt/scripts/entrypoint.sh

VOLUME ["/etc/letsencrypt"]

ENV PYTHONPATH=/app
ENV SSL_CERT_PATH=/etc/letsencrypt/live/jugger-tourna.de/fullchain.pem
ENV SSL_KEY_PATH=/etc/letsencrypt/live/jugger-tourna.de/privkey.pem

EXPOSE 8080

CMD ["/opt/scripts/entrypoint.sh"]
