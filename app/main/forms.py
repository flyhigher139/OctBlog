from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms import widgets, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo

from . import models

class PostForm(Form):
    title = StringField('Title', validators=[Required()])
    slug = StringField('Slug', validators=[Required()])
    raw = TextAreaField('Content')
    abstract = TextAreaField('Abstract')

    def validate_slug(self, field):
        if models.Post.objects.filter(slug=field.data).count() > 0:
            raise ValidationError('slug already in use')