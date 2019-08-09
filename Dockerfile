FROM python:3.7.3

ENV PYTHONUNBUFFERED=1 WORKDIR=/opt/docker_polls_group/api

RUN mkdir -p $WORKDIR
WORKDIR $WORKDIR
ADD . $WORKDIR

RUN pip install -r $WORKDIR/requirements/dev.txt
