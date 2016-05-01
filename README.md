# About OctBlog

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

### Backend

- jQuery
- BootStrap
    - [Clean Blog theme](http://startbootstrap.com/template-overviews/clean-blog/)
    - bootbox.js
    - bootstrap-markdown.js
    - bootstrap-datetimepicker.js
- Font Awesome
- highlight.js

##How to run OctBlog ?

###Run from source code

If you want to see more about the source code, checkout the [source code readme](app)


###Run by docker(recommended)

Run OctBlog by docker is recommended, here are some instruction：

####First Run

1\. Build your own OctBlog image

In command line, switch to OctBlog root directory, and run the following command to build your own OctBlog image:

```bash
(sudo) docker-compose build

#Now you can take a cup of coffee and wait for a few minutes :)
```

2\. Run OctBlog

```bash
(sudo) docker-compose up -d
```

Then you can visit OctBlog in your brower at `http://localhost:8000`

3\. Get into OctBlog container

Maybe you would like to dig into the container, the following command will help:

```bash
#Specify OctBlog container ID, eg:12345678
(sudo) docker ps

#Get into OctBlog container
(sudo) docker exec -it 12345678 bash

```

####After first run

- Start OctBlog

```bash
(sudo) docker-compose start
```

- Stop OctBlog

```bash
(sudo) docker-compose stop
```


###Get started with OctBlog

####1\. Create a superuser to administrate OctBlog

Visit the following url and create a superuser

`http://localhost:8000/accounts/registration/su`

If the url is forbidden, you need to modify your configurations to allow the creation.

####2\. Administrate OctBlog

The admin home is: `http://localhost:8000/admin`

You will be redirected to login page if you haven't logged in

####3\. Modify the default configurations

You either change settings in `app/OctBlog/config.py` file, or set environment variables defined in that file.

**Setting environment variables is recommended, and once the configuration is changed, you need to restart the service.**



## License

OctBlog is under [GPL2](https://github.com/flyhigher139/OctBlog/blob/dev/LICENSE)
