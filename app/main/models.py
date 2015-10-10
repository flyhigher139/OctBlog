import datetime
from flask import url_for

# from mongoengine import *

from OctBlog import db

class Post(db.Document):
    title = db.StringField(max_length=255, default='new blog', required=True)
    slug = db.StringField(max_length=255, required=True)
    abstract = db.StringField()
    raw = db.StringField(required=True)
    pub_time = db.DateTimeField(default=datetime.datetime.now, required=True)
    update_time = db.DateTimeField(default=datetime.datetime.now, required=True)
    content_html = db.StringField(required=True)
    # author = db.ForeignKey(User)
    # tags = db.ManyToManyField('Tag', blank=True)
    # category = db.ForeignKey('Category', null=True, blank=True)
    is_draft = db.BooleanField(default=False)

    def get_absolute_url(self):
        return url_for('post', kwargs={"slug": self.slug})

    def __unicode__(self):
        return self.title

    meta = {
        'allow_inheritance': True,
        'indexes': ['slug'],
        'ordering': ['-created_at']
    }