#!/bin/bash

docker-compose build --build-arg CACHEBUST=$(date +%s)
docker-compose down && docker-compose up -d
