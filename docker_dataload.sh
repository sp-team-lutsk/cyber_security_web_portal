#!/usr/bin/bash


docker-compose up -d
docker exec -it dpg_api python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); User.email='user@example.com'; User.set_password(password='Admin123!'); User.is_active=True; User.name='test_User'; User.save()"
docker-compose stop
