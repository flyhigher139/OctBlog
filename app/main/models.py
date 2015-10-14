import datetime
from flask import url_for

import markdown2

# from mongoengine import *

from OctBlog import db
from accounts.models import User

class Post(db.Document):
    title = db.StringField(max_length=255, default='new blog', required=True)
    slug = db.StringField(max_length=255, required=True, unique=True)
    abstract = db.StringField()
    raw = db.StringField(required=True)
    pub_time = db.DateTimeField(default=datetime.datetime.now(), required=True)
    update_time = db.DateTimeField(default=datetime.datetime.now(), required=True)
    content_html = db.StringField(required=True)
    author = db.ReferenceField(User)
    category = db.StringField(default='default')
    # tags = db.ManyToManyField('Tag', blank=True)
    is_draft = db.BooleanField(default=False)

    def get_absolute_url(self):
        return url_for('post_detail', kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.update_time = datetime.datetime.now()
        # self.content_html = self.raw
        self.content_html = markdown2.markdown(self.raw, extras=['code-friendly', 'fenced-code-blocks']).encode('utf-8')
        return super(Post, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    meta = {
        'allow_inheritance': True,
        'indexes': ['slug'],
        'ordering': ['-pub_time']
    }