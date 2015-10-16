from urlparse import urljoin
from flask import request, redirect, render_template, url_for, abort, flash
from flask.views import MethodView

from werkzeug.contrib.atom import AtomFeed

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

def make_external(url):
    return urljoin(request.url_root, url)

def recent_feed():
    feed = AtomFeed('Recent Articles', feed_url=request.url, url=request.url_root)

    posts = models.Post.objects.filter(post_type='post', is_draft=False)[:15]
    for post in posts:
        # return post.get_absolute_url()
        feed.add(post.title, unicode(post.content_html),
                 content_type='html',
                 author=post.author.username,
                 url=make_external(post.get_absolute_url()),
                 updated=post.update_time,
                 published=post.pub_time)
    return feed.get_response()
