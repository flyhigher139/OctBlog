#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from flask import url_for

import markdown2, bleach

from OctBlog import db
from accounts.models import User

def get_clean_html_content(html_content):
    allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'hr']
    html_content = bleach.linkify(bleach.clean(html_content, tags=allowed_tags, strip=True))
    return html_content



POST_TYPE_CHOICES = ('post', 'page', 'wechat')

class Post(db.Document):
    title = db.StringField(max_length=255, default='new blog', required=True)
    slug = db.StringField(max_length=255, required=True, unique=True)
    fix_slug = db.StringField(max_length=255, required=False)
    abstract = db.StringField()
    raw = db.StringField(required=True)
    pub_time = db.DateTimeField()
    update_time = db.DateTimeField()
    content_html = db.StringField(required=True)
    author = db.ReferenceField(User)
    category = db.StringField(max_length=64)
    tags = db.ListField(db.StringField(max_length=30))
    is_draft = db.BooleanField(default=False)
    post_type = db.StringField(max_length=64, default='post')

    def get_absolute_url(self):
        # return url_for('main.post_detail', slug=self.slug)

        router = {
            'post': url_for('main.post_detail', slug=self.slug, _external=True),
            'page': url_for('main.page_detail', slug=self.slug, _external=True),
            'wechat': url_for('main.wechat_detail', slug=self.slug, _external=True),
        }

        return router[self.post_type]

    def save(self, allow_set_time=False, *args, **kwargs):
        if not allow_set_time:
            now = datetime.datetime.now()
            if not self.pub_time:
                self.pub_time = now
            self.update_time = now
        # self.content_html = self.raw
        self.content_html = markdown2.markdown(self.raw, extras=['code-friendly', 'fenced-code-blocks', 'tables']).encode('utf-8')
        return super(Post, self).save(*args, **kwargs)

    def set_post_date(self, pub_time, update_time):
        self.pub_time = pub_time
        self.update_time = update_time
        return self.save(allow_set_time=True)

    def __unicode__(self):
        return self.title

    meta = {
        'allow_inheritance': True,
        'indexes': ['slug'],
        'ordering': ['-pub_time']
    }

# class Post(PostBase):
#     fix_slug = db.StringField(max_length=255, required=False)
#     category = db.StringField(max_length=64, default='default')
#     tags = db.ListField(db.StringField(max_length=30))
#     is_draft = db.BooleanField(default=False)

class Draft(db.Document):
    title = db.StringField(max_length=255, default='new blog', required=True)
    slug = db.StringField(max_length=255, required=True, unique=True)
    # fix_slug = db.StringField(max_length=255, required=False)
    abstract = db.StringField()
    raw = db.StringField(required=True)
    pub_time = db.DateTimeField()
    update_time = db.DateTimeField()
    content_html = db.StringField(required=True)
    author = db.ReferenceField(User)
    category = db.StringField(max_length=64, default='default')
    tags = db.ListField(db.StringField(max_length=30))
    is_draft = db.BooleanField(default=True)
    post_type = db.StringField(max_length=64, default='post')

    def save(self, *args, **kwargs):
        now = datetime.datetime.now()
        if not self.pub_time:
            self.pub_time = now
        self.update_time = now
        self.content_html = markdown2.markdown(self.raw, extras=['code-friendly', 'fenced-code-blocks', 'tables']).encode('utf-8')
        return super(Draft, self).save(*args, **kwargs)


    def __unicode__(self):
        return self.title

    meta = {
        'allow_inheritance': True,
        'indexes': ['slug'],
        'ordering': ['-update_time']
    }

class Tracker(db.Document):
    post = db.ReferenceField(Post)
    ip = db.StringField()
    user_agent = db.StringField()
    create_time = db.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.create_time:
            self.create_time = datetime.datetime.now()
        return super(Tracker, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.ip

    meta = {
        'allow_inheritance': True,
        'indexes': ['ip'],
        'ordering': ['-create_time']
    }


class PostStatistics(db.Document):
    post = db.ReferenceField(Post)
    visit_count = db.IntField(default=0)
    verbose_count_base = db.IntField(default=0)

class Widget(db.Document):
    title = db.StringField(default='widget')
    md_content = db.StringField()
    html_content = db.StringField()
    allow_post_types = db.ListField(db.StringField())
    update_time = db.DateTimeField()

    def save(self, *args, **kwargs):
        if self.md_content:
            self.html_content = markdown2.markdown(self.md_content, extras=['code-friendly', 'fenced-code-blocks', 'tables']).encode('utf-8')

        if not self.update_time:
            self.update_time = datetime.datetime.now()

        return super(Widget, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    meta = {
        # 'allow_inheritance': True,
        'ordering': ['update_time']
    }

COMMENT_STATUS = ('approved', 'pending', 'spam', 'deleted')
class Comment(db.Document):
    author = db.StringField(required=True)
    email = db.EmailField(max_length=255)
    homepage = db.URLField()
    # post = db.ReferenceField(Post)
    post_slug = db.StringField(required=True)
    post_title = db.StringField(default='default article')
    md_content = db.StringField()
    html_content = db.StringField()
    pub_time = db.DateTimeField()
    update_time = db.DateTimeField()
    replay_to = db.ReferenceField('self')
    status = db.StringField(choices=COMMENT_STATUS, default='pending')
    misc = db.StringField() # If the comment is imported, this field will store something useful

    def save(self, *args, **kwargs):
        if self.md_content:
            html_content = markdown2.markdown(self.md_content, extras=['code-friendly', 'fenced-code-blocks', 'tables', 'nofollow']).encode('utf-8')
            self.html_content = get_clean_html_content(html_content)

        if not self.pub_time:
            self.pub_time = datetime.datetime.now()

        self.update_time = datetime.datetime.now()

        return super(Comment, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.md_content[:64]

    meta = {
        'ordering': ['-update_time']
    }
