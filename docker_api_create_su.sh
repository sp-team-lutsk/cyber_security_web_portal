#!/bin/bash

docker-compose up -d
docker exec -it dpg_api python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin@example.com', 'Admin123!')"
docker-compose stop
