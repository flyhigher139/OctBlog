from flask import request, redirect, render_template, url_for, abort, flash
from flask.views import MethodView

from . import models


def test():
    return 'Test page'

def index():
    return 'Hello'

def list_posts():
    posts = models.Post.objects.all()

    tags = posts.distinct('tags')

    cur_category = request.args.get('category')
    cur_tag = request.args.get('tag')

    if cur_category:
        posts = posts.filter(category=cur_category)

    if cur_tag:
        posts = posts.filter(tags=cur_tag)

    #group by aggregate
    category_cursor = models.Post._get_collection().aggregate([
            { '$group' : 
                { '_id' : {'category' : '$category' }, 
                  'name' : { '$first' : '$category' },
                  'count' : { '$sum' : 1 },
                }
            }
        ])

    data = { 'posts':posts, 'cur_category':cur_category, 'category_cursor':category_cursor, 'cur_tag':cur_tag, 'tags':tags}
    return render_template('main/index.html', **data)

def post_detail(slug):
    try:
        post = models.Post.objects.get(slug=slug)
    except models.Post.DoesNotExist:
        abort(404)
        
    return render_template('main/post.html', post=post)
