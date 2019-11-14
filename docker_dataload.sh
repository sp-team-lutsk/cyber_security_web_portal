#!/usr/bin/bash


docker-compose up -d
docker exec -it dpg_api python manage.py shell -c "from authentication.models import StdUser; User=StdUser(); User.email='user@example.com'; User.set_password('Admin123!'); User.is_active=True; User.name='test_User'; User.save()"
docker-compose stop
