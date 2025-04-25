#!/bin/bash

certbot renew --quiet

docker compose exec frontend nginx -s reload
