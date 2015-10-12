from flask import request, redirect, render_template, url_for, abort
from flask.views import MethodView

from . import models

##################################
# Blog View
##################################

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
        return render_template('main/post.html', post=post)
    except models.Post.DoesNotExist:
        abort(404)

#######################################
# Blog Admin
#######################################

class AdminIndex(MethodView):
    template_name = 'blog_admin/index.html'
    def get(self):
        return render_template(self.template_name)