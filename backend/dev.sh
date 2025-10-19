#!/bin/bash

PORT=33500 \
GIN_MODE=dev \
DB_USER=root \
POSTGRES_PASSWORD=example \
POSTGRES_DB=contacts_db \
docker compose \
-f compose.dev.yml \
up -d