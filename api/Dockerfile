FROM python:3.7.3

ENV PYTHONUNBUFFERED=1 WORKDIR=/opt/docker_polls_group/api

RUN mkdir -p $WORKDIR
WORKDIR $WORKDIR
ADD . $WORKDIR

RUN apt-get install python3-dev
RUN pip install --upgrade pip
RUN pip install -r $WORKDIR/requirements/dev.txt

RUN apt-get update
RUN apt-get install -y cron

CMD python manage.py runserver
