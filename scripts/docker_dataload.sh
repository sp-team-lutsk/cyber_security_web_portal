#!/bin/bash


docker-compose up -d

docker exec -it dpg_api python manage.py shell -c "from authentication.models import StdUser; Admin=StdUser(); Admin.email='admin@example.com'; Admin.set_password('Admin123!'); Admin.is_active=True; Admin.is_admin=True; Admin.first_name='test_Admin'; Admin.save()"

docker exec -it dpg_api python manage.py shell -c "from authentication.models import StdUser; Moderator=StdUser(); Moderator.email='moderator@example.com'; Moderator.set_password('Admin123!'); Moderator.is_active=True; Moderator.is_moderator=True; Moderator.first_name='test_Moderator'; Moderator.save()"

docker exec -it dpg_api python manage.py shell -c "from authentication.models import StdUser; User=StdUser(); User.email='user@example.com'; User.set_password('Admin123!'); User.is_active=True; User.first_name='test_User'; User.save()"

docker exec -it dpg_api python manage.py shell -c "from authentication.models import StdUser,Faculty,Profession; f=Faculty.objects.create(name='KNIT');p=Profession.objects.create(name='cybersecurity');StdUser.objects.create_teacher(email='teacher@example.com',password='Admin123!',faculty=f)"

docker exec -it dpg_api python manage.py shell -c "from authentication.models import StdUser,Profession,Faculty; Student=StdUser; Student.objects.create_student(email='student@example.com',password='Admin123!',profession=Profession.objects.get(name='cybersecurity'),faculty=Faculty.objects.get(name='KNIT')) "

for i in 1 2 3 4 5
do
docker exec -it dpg_api python manage.py shell -c "from ext_news.models import News; news=News(); news.title='Test_News_$i'; news.description='description'; news.news_link='localhost/'; news.images_link='localhost/'; news.is_checked=True; news.save()"
done

for i in 1 2 3 4 5
do
    docker exec -it dpg_api python manage.py shell -c "from int_news.models import NewsInt; from authentication.models import StdUser; author = StdUser.objects.get(email='moderator@example.com'); news=NewsInt(); news.title='Test_News_$i'; news.author=author;news.content='content'; news.is_checked=True; news.save()"
done


docker-compose stop
