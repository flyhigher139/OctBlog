from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SelectField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo

from . import models

class LoginForm(Form):
    username = StringField()
    password = PasswordField()
    remember_me = BooleanField('Keep me logged in')

class RegistrationForm(Form):
    username = StringField('Username', validators=[Required(), Length(1,64), 
        Regexp('^[A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers dots or underscores')])
    email = StringField('Email', validators=[Required(), Length(1,128), Email()])
    password = PasswordField('Password', validators=[Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[Required()])

    def validate_username(self, field):
        if models.User.objects.filter(username=field.data).count() > 0:
            raise ValidationError('Username already in use')

    def validate_email(self, field):
        if models.User.objects.filter(email=field.data).count() > 0:
            raise ValidationError('Email already in registered')

class UserForm(Form):
    email = StringField('Email', validators=[Required(), Length(1,128), Email()])
    # is_active = BooleanField('Is activie')
    is_superuser = BooleanField('Is superuser')
    role = SelectField('Role', choices=models.ROLES)