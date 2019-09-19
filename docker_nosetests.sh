#!/bin/bash

rm -rf htmlcov/
docker exec -it dpg_api coverage run --omit='*/migrations/*.py,*__init__*,wsgi.py,manage.py' --source='.' manage.py test authentication ext_news
docker exec -it dpg_api coverage report
docker exec -it dpg_api coverage html
docker cp dpg_api:/opt/docker_polls_group/api/htmlcov ./htmlcov
docker exec -it dpg_api coverage erase
