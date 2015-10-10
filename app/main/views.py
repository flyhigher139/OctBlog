from flask import request, redirect, render_template, url_for
from flask.views import MethodView

from . import models

def test():
    return 'Test page'

def index():
    return 'Hello'

def list_posts():
    posts = models.Post.objects.all()
    # return posts[0].slug
    return render_template('main/index.html', posts=posts)