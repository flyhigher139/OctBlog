from flask import request, redirect, render_template, url_for, abort, flash
from flask.views import MethodView

from . import models


def test():
    return 'Test page'

def index():
    return 'Hello'

def list_posts():
    posts = models.Post.objects.all()
    return render_template('main/index.html', posts=posts)

def post_detail(slug):
    try:
        post = models.Post.objects.get(slug=slug)
    except models.Post.DoesNotExist:
        abort(404)
        
    return render_template('main/post.html', post=post)
