#!/bin/bash

EXCLUDE='*/migrations/*.py,*/__init__.py,*/adapter.py,*/apps.py,*/cron.py,*/permissions.py,*/validators.py,*/tests/*.py,*/admin.py,*/parsing.py,wsgi.py,manage.py,*/utils/*.py,*/settings/*.py'

rm -rf htmlcov/
docker exec -it dpg_api coverage run --omit=$EXCLUDE --source='.' manage.py test authentication.tests int_news.tests ext_news.tests

docker exec -it dpg_api coverage html
docker cp dpg_api:/opt/docker_polls_group/api/htmlcov ./htmlcov
docker exec -it dpg_api coverage erase
