# MAINTAINER        Gevin <flyhigher139@gmail.com>
# DOCKER-VERSION    1.8.2
#
# Dockerizing Ubuntu: Dockerfile for building Ubuntu images
FROM       ubuntu:14.04
MAINTAINER Gevin <flyhigher139@gmail.com>
# ADD sources.list /etc/apt/sources.list

RUN apt-get update && apt-get install -y vim && \
    apt-get install -y nginx build-essential python-dev python-pip && \
    apt-get clean all

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN pip install -U pip
RUN pip install --no-cache-dir supervisor gunicorn
ADD supervisord.conf /etc/supervisord.conf
RUN mkdir -p /etc/supervisor.conf.d && \
    mkdir -p /var/log/supervisor
RUN mkdir -p /usr/src/app && mkdir -p /var/log/gunicorn
WORKDIR /usr/src/app
ADD requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

COPY . /usr/src/app
RUN ln -s /usr/src/app/octblog_nginx.conf /etc/nginx/sites-enabled

EXPOSE 8000 5000

# CMD ["/bin/bash", "/usr/src/app/init.sh"]
# CMD ["/bin/bash"]
CMD ["/usr/local/bin/supervisord", "-n"]
# CMD ["/usr/bin/python2.7", "manage.py", "runserver"]