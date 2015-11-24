#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from flask import render_template, redirect, request, flash, url_for, current_app, session
from flask.views import MethodView
from flask.ext.login import login_user, logout_user, login_required, current_user
from flask.ext.principal import Identity, AnonymousIdentity, identity_changed

from . import models, forms
from permissions import admin_permission
from OctBlog.config import OctBlogSettings

def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.objects.get(username=form.username.data)
        except models.User.DoesNotExist:
            user = None

        if user and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            user.last_login = datetime.datetime.now
            user.save()
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.username))
            return redirect(request.args.get('next') or url_for('blog_admin.index'))

        flash('Invalid username or password', 'danger')

    return render_template('accounts/login.html', form=form)

@login_required
def logout():
    logout_user()
    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())

    flash('You have been logged out', 'success')
    return redirect(url_for('accounts.login'))

def register(create_su=False):
    if not OctBlogSettings['allow_registration']:
        msg = 'Register is forbidden, please contact administrator'
        return msg

    if create_su and not OctBlogSettings['allow_su_creation']:
        msg = 'Register superuser is forbidden, please contact administrator'
        return msg
        
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = models.User()
        user.username = form.username.data
        user.password = form.password.data
        user.email = form.email.data
        if create_su and OctBlogSettings['allow_su_creation']:
            user.is_superuser = True
        user.save()

        return redirect(url_for('main.index'))

    return render_template('accounts/registration.html', form=form)

@login_required
def add_user():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = models.User()
        user.username = form.username.data
        user.password = form.password.data
        user.email = form.email.data
        user.save()

        return redirect(url_for('blog_admin.index'))

    return render_template('accounts/registration.html', form=form)

def get_current_user():
    user = models.User.objects.get(username=current_user.username)
    return user


class Users(MethodView):
    decorators = [login_required, admin_permission.require(401)]
    template_name = 'accounts/users.html'
    def get(self):
        users = models.User.objects.all()
        return render_template(self.template_name, users=users)

class User(MethodView):
    decorators = [login_required, admin_permission.require(401)]
    template_name = 'accounts/user.html'

    def get_context(self, username, form=None):
        if not form:
            user = models.User.objects.get_or_404(username=username)
            form = forms.UserForm(obj=user)
        data = {'form':form}
        return data

    def get(self, username, form=None):
        data = self.get_context(username, form)
        return render_template(self.template_name, **data)

    def post(self, username):
        form = forms.UserForm(obj=request.form)
        if form.validate():
            user = models.User.objects.get_or_404(username=username)
            if user.email != form.email.data:
                user.is_email_confirmed = False
            user.email = form.email.data
            # user.is_active = form.is_active.data
            user.is_superuser = form.is_superuser.data
            user.role = form.role.data
            user.save()
            flash('Succeed to update user details', 'success')
            return redirect(url_for('accounts.edit_user', username=username))
        return self.get(username, form)

    def delete(self, username):
        user = models.User.objects.get_or_404(username=username)
        user.delete()

        if request.args.get('ajax'):
            return 'success'

        msg = 'Succeed to delete user'

        flash(msg, 'success')
        return redirect(url_for('accounts.users'))