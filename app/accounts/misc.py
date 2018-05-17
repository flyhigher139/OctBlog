#!/usr/bin/env python
# -*- coding: utf-8 -*-
from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from OctBlog import mail

def send_user_confirm_mail(to, user, token):
    title = 'OctBlog confirm user email'
    msg = Message(title)
    msg.sender = current_app._get_current_object().config['MAIL_USERNAME']
    msg.recipients = [to]

    template_name = 'accounts/confirm.txt'

    msg.body = render_template(template_name, user=user, token=token)
    msg.html = render_template(template_name, user=user, token=token)
        
    mail.send(msg)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template_txt, template_html=None, **kwargs):
    app = current_app._get_current_object()

    msg = Message(subject)
    msg.sender = current_app._get_current_object().config['MAIL_USERNAME']
    msg.recipients = [to]

    if not template_html:
        template_html = template_txt

    msg.body = render_template(template_txt, **kwargs)
    msg.html = render_template(template_html, **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

def send_user_confirm_mail2(to, user, token):
    title = 'OctBlog confirm user email'
    template_txt = 'accounts/confirm.txt'

    return send_email(to, title, template_txt, user=user, token=token)

def send_reset_password_mail(to, user, token):
    title = 'OctBlog reset password'
    template_txt = 'accounts/email/reset_password.txt'
    template_html = 'accounts/email/reset_password.html'

    return send_email(to, title, template_txt, template_html, user=user, token=token)
    