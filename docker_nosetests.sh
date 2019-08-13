#!/bin/bash

docker exec -it dpg_api coverage run --omit='*/migrations/*.py' --source='.' manage.py test authentication
docker exec -it dpg_api coverage report
docker exec -it dpg_api coverage erase