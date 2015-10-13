from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, HiddenField
from wtforms import widgets, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo

from . import models

class PostForm(Form):
    title = StringField('Title', validators=[Required()])
    slug = StringField('Slug', validators=[Required()])
    raw = TextAreaField('Content')
    abstract = TextAreaField('Abstract')
    post_id = HiddenField('post_id')

    def validate_slug(self, field):
        posts = models.Post.objects.filter(slug=field.data)
        if posts.count() > 0:
            if not self.post_id.data or str(posts[0].id) != self.post_id.data:
                raise ValidationError('slug already in use')
