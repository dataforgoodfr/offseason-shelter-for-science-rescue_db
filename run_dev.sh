#!/bin/bash

sudo docker compose --project-name rescue_db -f docker-compose.yml -f docker-compose.dev.yml up -d $@
