#!/bin/bash


docker-compose up -d

docker exec -it dpg_api python manage.py shell -c "from authentication.models import StdUser; Moderator=StdUser(); Moderator.email='moderator@example.com'; Moderator.set_password('Admin123!'); Moderator.is_active=True; Moderator.is_moderator=True; Moderator.first_name='test_Moderator'; Moderator.save()"

docker exec -it dpg_api python manage.py shell -c "from authentication.models import StdUser; User=StdUser(); User.email='user@example.com'; User.set_password('Admin123!'); User.is_active=True; User.first_name='test_User'; User.save()"

docker exec -it dpg_api python manage.py shell -c "from authentication.models import StdUser,Faculty,Profession; faculty=Faculty.objects.create(name='KNIT');profession=Profession.objects.create(name='cybersecurity');Teacher=StdUser();Teacher.create_teacher(email='teacher@example.com',password='Admin123!',faculty=Faculty.objects.get(name='KNIT'))"

docker exec -it dpg_api python manage.py shell -c "from authentication.models import StdUser,Profession,Faculty; Student=StdUser(); Student.create_student(email='student@example.com',password='Admin123!',profession=Profession.objects.get(name='cybersecurity'),faculty=Faculty.objects.get(name='KNIT')); "

for i in 1 2 3 4 5 
do
docker exec -it dpg_api python manage.py shell -c "from ext_news.models import News; news=News(); news.title='Test_News_$i'; news.description='description'; news.news_link='localhost/'; news.images_link='localhost/'; news.is_checked=True; news.save()"
done

for i in 1 2 3 4 5 
do
    docker exec -it dpg_api python manage.py shell -c "from int_news.models import NewsInt; from authentication.models import StdUser; author = StdUser.objects.get(email='moderator@example.com'); news=NewsInt(); news.title='Test_News_$i'; news.author=author;news.content='content'; news.is_checked=True; news.save()"
done


docker-compose stop
