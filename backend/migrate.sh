#!/bin/bash

atlas schema apply \
  -u "postgres://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}?sslmode=disable" \
  --to file://sql/schema.sql \
  --dev-url "docker://postgres/18/contacts_db"