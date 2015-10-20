from flask import render_template, redirect, request, flash, url_for, current_app, session
from flask.ext.login import login_user, logout_user, login_required, current_user
from flask.ext.principal import Identity, AnonymousIdentity, identity_changed

from . import models, forms
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
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.username))
            return redirect(request.args.get('next') or url_for('blog_admin.index'))

        flash('Invalid username or password', 'danger')

    return render_template('blog_admin/login.html', form=form)

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

def register():
    if not OctBlogSettings['allow_registration']:
        msg = 'Register is forbidden, please contact administrator'
        return msg
        
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = models.User()
        user.username = form.username.data
        user.password = form.password.data
        user.email = form.email.data
        user.save()

        return redirect(url_for('main.index'))

    return render_template('blog_admin/registration.html', form=form)

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

    return render_template('blog_admin/registration.html', form=form)

def get_current_user():
    user = models.User.objects.get(username=current_user.username)
    return user