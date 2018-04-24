# MAINTAINER        Gevin <flyhigher139@gmail.com>
# DOCKER-VERSION    18.03.0-ce, build 0520e24

FROM python:3.6.5-alpine3.7
LABEL maintainer="flyhigher139@gmail.com"
COPY pip.conf /root/.pip/pip.conf

RUN mkdir -p /usr/src/app  && \
    mkdir -p /var/log/gunicorn

WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/requirements.txt

RUN pip install --no-cache-dir gunicorn && \
    pip install --no-cache-dir -r /usr/src/app/requirements.txt && \
    pip install --ignore-installed six

COPY . /usr/src/app


ENV PORT 8000
EXPOSE 8000 5000

CMD ["/usr/local/bin/gunicorn", "-w", "2", "-b", ":8000", "manage:app"]