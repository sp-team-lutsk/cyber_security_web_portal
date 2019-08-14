#!/bin/bash

rm -rf htmlcov/
docker exec -it dpg_api coverage run --omit='*/migrations/*.py' --source='.' manage.py test authentication
docker exec -it dpg_api coverage report
docker exec -it dpg_api coverage html
docker cp dpg_api:/opt/docker_polls_group/api/htmlcov ./htmlcov
docker exec -it dpg_api coverage erase