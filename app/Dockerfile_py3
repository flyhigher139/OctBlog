# MAINTAINER        Gevin <flyhigher139@gmail.com>
# DOCKER-VERSION    18.03.0-ce, build 0520e24

FROM ubuntu:14.04
LABEL maintainer="flyhigher139@gmail.com"
COPY sources.list /etc/apt/sources.list
COPY pip.conf /root/.pip/pip.conf

RUN apt-get update && apt-get install -y \
    build-essential \
    python3 \
    python3-dev \
    python3-pip \
    && apt-get clean all \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install -U pip 

RUN mkdir -p /etc/supervisor.conf.d && \
    mkdir -p /var/log/supervisor  && \
    mkdir -p /usr/src/app  && \
    mkdir -p /var/log/gunicorn

WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/requirements.txt

RUN pip3 install --no-cache-dir gunicorn && \
    pip3 install --no-cache-dir -r /usr/src/app/requirements.txt && \
    pip3 install --ignore-installed six

COPY . /usr/src/app


ENV PORT 8000
EXPOSE 8000 5000

CMD ["/usr/local/bin/gunicorn", "-w", "2", "-b", ":8000", "manage:app"]