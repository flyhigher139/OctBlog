# MAINTAINER        Gevin <flyhigher139@gmail.com>
# DOCKER-VERSION    18.03.0-ce, build 0520e24

FROM ubuntu:14.04
LABEL maintainer="flyhigher139@gmail.com"
COPY sources.list /etc/apt/sources.list
COPY pip.conf /root/.pip/pip.conf

RUN apt-get update && apt-get install -y \
    vim \
    nginx \
    build-essential \
    python-dev \
    python-pip \
    # && apt-get clean all
    && rm -rf /var/lib/apt/lists/* \
    && pip install -U pip 

RUN mkdir -p /etc/supervisor.conf.d && \
    mkdir -p /var/log/supervisor  && \
    mkdir -p /usr/src/app  && \
    mkdir -p /var/log/gunicorn

WORKDIR /usr/src/app
COPY . /usr/src/app

RUN pip install --no-cache-dir supervisor gunicorn &&\
    pip install --no-cache-dir -r /usr/src/app/requirements.txt


RUN echo "daemon off;" >> /etc/nginx/nginx.conf && \
    ln -s /usr/src/app/octblog_nginx.conf /etc/nginx/sites-enabled

EXPOSE 8000 5000

# CMD ["/usr/local/bin/supervisord", "-n"]
CMD ["/usr/local/bin/supervisord", "-c", "supervisord.conf"]