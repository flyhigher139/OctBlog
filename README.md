# About OctBlog

[OctBlog](https://github.com/flyhigher139/OctBlog) is almost the same with [MayBlog](https://github.com/flyhigher139/mayblog) except that it is powered by [Flask](http://flask.pocoo.org/) and [MongoDB](https://www.mongodb.org/) rather than [Django](https://www.djangoproject.com/) and SQL Databases.

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

## License

OctBlog is under [GPL2](https://github.com/flyhigher139/mayblog/blob/dev/LICENSE)
