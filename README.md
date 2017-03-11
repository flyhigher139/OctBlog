# About OctBlog

[![](https://images.microbadger.com/badges/image/gevin/octblog.svg)](http://microbadger.com/images/gevin/octblog "Get your own image badge on microbadger.com") [![](https://images.microbadger.com/badges/version/gevin/octblog.svg)](http://microbadger.com/images/gevin/octblog "Get your own version badge on microbadger.com")

[OctBlog](https://github.com/flyhigher139/OctBlog) is almost the same with [MayBlog](https://github.com/flyhigher139/MayBlog) except that it is powered by [Flask](http://flask.pocoo.org/) and [MongoDB](https://www.mongodb.org/) rather than [Django](https://www.djangoproject.com/) and SQL Databases.

And as my customary, I named it OctBlog as OctBlog was started in October, 2015

OctBlog offers every function in MayBlog, and aims to do it better, its features are as follow:

- multiple user
- roles: su, admin, editor, writer, reader
- posts, pages, tags, and categories
- markdown support
- admin interface
- change configurations by configuration file or environment variable
- multiple comment plugin
- RESTful API(not yet)
- Deploy with docker

## Demo

[Gevin's blog](http://gevin-oct-blog.daoapp.io/) is powered by OctBlog

## Dependency

### Backend

- Flask
    - flask-script
    - flask-login
    - flask-admin
    - Flask-WTF
    - flask-principal
    - flask_mongoengine
- WTForms
- mongoengine
- markdown2
- bleach

### Frontend

- jQuery
- BootStrap
    - [Clean Blog theme](http://startbootstrap.com/template-overviews/clean-blog/)
    - bootbox.js
    - bootstrap-markdown.js
    - bootstrap-datetimepicker.js
- Font Awesome
- highlight.js

## How to run OctBlog ?

### Run from source code

If you want to see more about the source code, checkout the [source code readme](app)


### Run by docker(recommended)

Run OctBlog by docker is recommended, here are some instruction：

#### First Run

1\. Get your OctBlog image

In command line, switch to OctBlog root directory, and run the following command to build your own OctBlog image:

```bash
cd app
(sudo) docker build gevin/octblog:0.1 .

# Now you can take a cup of coffee and wait for a few minutes :)
```

Alternatively, pull Octblog image from DockerHub(**recommended**):

```bash
(sudo) docker pull gevin/octblog:0.1
```

2\. Run OctBlog

```bash
(sudo) docker-compose up -d
```

Then you can visit OctBlog in your brower at `http://localhost:8000`

All environment variables can be found in `/OctBlog/config.py`

A `.env` file example:

```
config=prd
MONGO_HOST=mongo
allow_registration=true
allow_su_creation=true

wechat_subtitle=技术、生活都要折腾
subtitle=技术、生活都要折腾
description=技术、生活都要折腾
wechat_name=GevinView @ <i class="fa fa-weixin" aria-hidden="true"></i>
copyright_msg=注：转载本文，请与Gevin联系
donation_msg=如果您觉得Gevin的文章有价值，就请Gevin喝杯茶吧！
DEBUG=false
google_site_verification=Cj8n-gGgBXzrcuYXoe9fWtDOqNn0hmakKzmoazwrFAY
allow_comment=true
wechat_msg=欢迎关注我的微信公众账号
name=Gevin's Blog
```

3\. Get into OctBlog container

Maybe you would like to dig into the container, the following command will help:

```bash
# Specify OctBlog container ID, eg:12345678
(sudo) docker ps

# Get into OctBlog container
(sudo) docker exec -it 12345678 bash

```

#### After first run

- Start OctBlog

```bash
(sudo) docker-compose start
```

- Stop OctBlog

```bash
(sudo) docker-compose stop
```


### Get started with OctBlog

#### 1\. Create a superuser to administrate OctBlog

Visit the following url and create a superuser

`http://localhost:8000/accounts/registration/su`

If the url is forbidden, you need to modify your configurations to allow the creation.

#### 2\. Administrate OctBlog

The admin home is: `http://localhost:8000/admin`

You will be redirected to login page if you haven't logged in

#### 3\. Modify the default configurations

You either change settings in `app/OctBlog/config.py` file, or set environment variables defined in that file.

**Setting environment variables is recommended, and once the configuration is changed, you need to restart the service.**



## License

OctBlog is under [GPL2](https://github.com/flyhigher139/OctBlog/blob/dev/LICENSE)
