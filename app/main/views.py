from flask import request, redirect, render_template, url_for, abort, flash
from flask.views import MethodView

from . import models


def test():
    return 'Test page'

def index():
    return 'Hello'

def list_posts():
    posts = models.Post.objects.all()
    categories = posts.distinct('category')
    cur_category = request.args.get('category')
    if cur_category:
        posts = posts.filter(category=cur_category)

    data = { 'posts':posts, 'categories':categories, 'cur_category':cur_category}
    return render_template('main/index.html', **data)

def post_detail(slug):
    try:
        post = models.Post.objects.get(slug=slug)
    except models.Post.DoesNotExist:
        abort(404)
        
    return render_template('main/post.html', post=post)
