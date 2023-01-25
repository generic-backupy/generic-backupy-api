#!/bin/bash
docker compose --env-file .env -f docker-compose/docker-compose.locust.yml $@
