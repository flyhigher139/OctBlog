from flask import render_template, redirect, request, flash, url_for
from flask.ext.login import login_user, logout_user, login_required

from . import models, forms

def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.objects.get(username=form.username.data)
        except models.User.DoesNotExist:
            user = None

        if user and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or password')

    return render_template('accounts/login.html', form=form)

@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))