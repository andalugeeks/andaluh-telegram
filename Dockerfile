FROM python:3.6

LABEL maintainer="felixonta@gmail.com"

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
        libatlas-base-dev gfortran nginx supervisor

RUN pip install uwsgi

COPY ./requirements.txt /project/requirements.txt
RUN pip install -r /project/requirements.txt

RUN useradd --no-create-home nginx

RUN rm /etc/nginx/sites-enabled/default
RUN rm -r /root/.cache

COPY nginx.conf /etc/nginx/
COPY site-nginx.conf /etc/nginx/conf.d/
COPY uwsgi.ini /etc/uwsgi/
COPY supervisord.conf /etc/

COPY app /project/app

WORKDIR /project

CMD ["/usr/bin/supervisord"]
