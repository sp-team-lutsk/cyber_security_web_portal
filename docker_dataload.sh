#!/usr/bin/bash


docker-compose up -d

docker exec -it dpg_api python manage.py shell -c "from authentication.models import StdUser; Moderator=StdUser(); Moderator.email='moderator@example.com'; Moderator.set_password('Admin123!'); Moderator.is_active=True; Moderator.is_moderator=True; Moderator.name='test_Moderator'; Moderator.save()"

docker exec -it dpg_api python manage.py shell -c "from authentication.models import StdUser; User=StdUser(); User.email='user@example.com'; User.set_password('Admin123!'); User.is_active=True; User.name='test_User'; User.save()"

docker exec -it dpg_api python manage.py shell -c "from authentication.models import StdUser; Teacher=StdUser();Teacher.email='teacher@example.com'; Teacher.set_password('Admin123!'); Teacher.is_active=True; Teacher.is_teacher=True; Teacher.name='test_Teacher'; Teacher.save()"

docker exec -it dpg_api python manage.py shell -c "from authentication.models import StdUser; Student=StdUser();Student.email='student@example.com'; Student.set_password('Admin123!'); Student.is_active=True; Student.is_student=True; Student.name='test_Student'; Student.save()"


docker exec -it dpg_api python manage.py shell -c "from ext_news.models import News; news=News(); news.title='Test_News_1'; news.description='description'; news.news_link='localhost/'; news.images_link=None; news.is_checked=True; news.save()"


docker-compose stop
