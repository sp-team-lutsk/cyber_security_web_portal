FROM python:3.7.3
ENV PYTHONUNBUFFERED 1
RUN mkdir /docker_polls_group/
WORKDIR /docker_polls_group/
ADD . /docker_polls_group/
RUN pip install -r /docker_polls_group/requirements/base.txt
CMD python manage.py runserver localhost:8000
CMD python manage.py makemigrations
CMD command: python manage.py migrate