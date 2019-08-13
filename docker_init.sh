#!/bin/bash

echo "Building Docker"

docker-compose build
docker-compose up -d
docker-compose stop