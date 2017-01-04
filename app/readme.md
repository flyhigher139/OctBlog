Welcome to OctBlog
====================

>OctBlog is powered by Flask and MongoDB, here are some instructions on how to run it.

## How to run it ?

### Install requirements

```
(sudo) pip install -r requirements.txt
```

### Create/update datebase

MongoDB is flexible, migrating database is not necessary.


### Run OctBlog

Run OctBlog with this command:

```bash
python manage.py runserver
```

Then you can visit the blog with url: `http://127.0.0.1:5000`

If you want to customize `manage.py`, checkout [Flask-Script](https://flask-script.readthedocs.org/en/latest/)

### Get started with OctBlog

#### 1\. Create a superuser to administrate OctBlog

Visit the following url and create a superuser

`http://127.0.0.1:5000/accounts/registration/su`

If the url is forbidden, you need to modify your configurations to allow the creation.

#### 2\. Administrate OctBlog

The admin home is: `http://127.0.0.1:5000/admin`

You will be redirected to login page if you haven't logged in

#### 3\. Modify the default configurations

You either change settings in `app/OctBlog/config.py` file, or set the environment variables defined in this file.

**Setting environment variables is recommended, and once the configuration is changed, you need to restart the service.**


### OctBlog settings

By default, OctBlog uses `dev` settings, `prd` is used in product environment. You can overwrite these settings or create your custom settings and switch to it.

#### How to switch settings

If you don't want to use the default settings, just set a settings environment vairable.

I usually set the environment vairable in bash with `export` command. For example, if I want to run OctBlog in product environment, I will switch to prd settings like this:

```
export config=prd
```

## Deploy OctBlog

I recommend you to deploy OctBlog by `Ubuntu + nginx + gunicorn`.

[Here](http://flask.pocoo.org/docs/0.10/deploying/wsgi-standalone/) is an instruction, and it is enough.

*Deploying OctBlog with docker is another recommended option*

### What's more

If you find a bug or want to add a new feature, just issue me.

Want to contribute? Please fork OctBlog and pull request to me.

I'm not good at frontend development, so I used a free bootstrap blog theme. If you can redesign the blog theme and admin interface, I'll appriciate your work very much!
