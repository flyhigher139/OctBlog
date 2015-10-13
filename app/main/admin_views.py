from flask import request, redirect, render_template, url_for, abort, flash
from flask.views import MethodView

from . import models

class AdminIndex(MethodView):
    template_name = 'blog_admin/index.html'
    def get(self):
        return render_template(self.template_name)

class PostsList(MethodView):
    template_name = 'blog_admin/posts.html'
    def get(self):
        posts = models.Post.objects.filter(is_draft=False)

        return render_template(self.template_name, posts=posts)