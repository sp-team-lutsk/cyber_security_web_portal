#!/bin/bash

echo -e "\n[ Cleaning docker ]\n"

echo "Stoping docker"                                
docker-compose stop                                  
                                                     
echo "Removing Compose containers"                   
docker-compose rm --all -f                           
                                                     
docker-compose ps                                    
                                                     
docker ps                                            
                                                     
echo "Removing Docker containers, images and volumes"
                                                     
docker stop $(docker ps -a -q)                       
docker rm -f $(docker ps -a -q)                      
docker rmi -f $(docker images -q)                    
docker volume rm -f $(docker volume ls  -q)         

echo -e "\n[ Building Docker ]\n"

docker-compose build

echo -e "\n[ Starting Docker Compose ]\n"
docker-compose up -d

echo -e "\n[ Updating Docker Database ]\n"
docker exec dpg_api python manage.py makemigrations authentication
docker exec dpg_api python manage.py migrate --noinput      

echo -e "\n[ Collecting static files ]\n"
docker exec dpg_api python manage.py collectstatic

echo -e "\n[ Creating superuser ]\n"
docker exec -it dpg_api python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin@example.com', 'Admin123!')"        

echo "Email: admin@example.com"
echo "Password: Admin123!"
