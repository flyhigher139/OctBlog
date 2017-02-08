#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from flask.ext.mongoengine.wtf import model_form
from flask_mongoengine.wtf import model_form
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, HiddenField, RadioField, FileField, IntegerField
from wtforms import widgets, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, URL, Optional

from . import models

class PostForm(FlaskForm):
    title = StringField('Title', validators=[Required()])
    slug = StringField('Slug', validators=[Required()])
    raw = TextAreaField('Content')
    abstract = TextAreaField('Abstract')
    category = StringField('Category')
    tags_str = StringField('Tags')
    post_id = HiddenField('post_id')
    post_type = HiddenField('post_type')
    from_draft = HiddenField('from_draft')

    def validate_slug(self, field):
        if self.from_draft.data and self.from_draft.data == 'true':
            posts = models.Draft.objects.filter(slug=field.data)
        else:
            posts = models.Post.objects.filter(slug=field.data)
        if posts.count() > 0:
            if not self.post_id.data or str(posts[0].id) != self.post_id.data:
                raise ValidationError('slug already in use')

SuPostForm = model_form(models.Post, exclude=['pub_time', 'update_time', 'content_html', 'category', 'tags', 'post_type'])

class WidgetForm(FlaskForm):
    title = StringField('Title', validators=[Required()])
    content = TextAreaField('Content', validators=[Required()])
    content_type = RadioField('Content Type', choices=[('markdown', 'markdown'), ('html', 'html')], default='html')
    priority = IntegerField(default=1000000)

class CommentForm(FlaskForm):
    email = StringField('* Email', validators=[Required(), Length(1,128), Email()])
    author = StringField('* Name', validators=[Required(), Length(1,128)])
    homepage = StringField('Homepage', validators=[URL(), Optional()])
    content = TextAreaField('* Comment <small><span class="label label-info">markdown</span></small>', validators=[Required()])
    comment_id = HiddenField('comment_id')

class SessionCommentForm(FlaskForm):
    email = HiddenField('* Email')
    author = HiddenField('* Name')
    homepage = HiddenField('Homepage')
    content = TextAreaField('* Comment', validators=[Required()])
    comment_id = HiddenField('comment_id')

class ImportCommentForm(FlaskForm):
    content = TextAreaField('Content')
    json_file = FileField('Json File')
    import_format = RadioField('Import Format', choices=[('text', 'text'), ('file', 'file')], default='text')