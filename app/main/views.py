from flask import request, redirect, render_template, url_for, abort, flash
from flask.views import MethodView

from . import models
from OctBlog.config import OctBlogSettings


def get_base_data():
    pages = models.Post.objects.filter(post_type='page', is_draft=False)
    blog_meta = OctBlogSettings['blog_meta']
    data = {'blog_meta':blog_meta, 'pages':pages}
    return data

def index():
    return 'Hello'

def list_posts():
    posts = models.Post.objects.filter(post_type='post', is_draft=False)

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

    data = get_base_data()
    data['posts'] = posts
    data['cur_category'] = cur_category
    data['category_cursor'] = category_cursor
    data['cur_tag'] = cur_tag
    data['tags'] = tags

    return render_template('main/index.html', **data)

def post_detail(slug, post_type='post'):
    try:
        post = models.Post.objects.get(slug=slug, post_type=post_type)
    except models.Post.DoesNotExist:
        abort(404)

    data = get_base_data()
    data['post'] = post
    return render_template('main/post.html', **data)
