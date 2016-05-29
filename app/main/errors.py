from flask import render_template

from .views import get_base_data

def handle_unmatchable(*args, **kwargs):
    # return 'unmatchable page', 404
    data = get_base_data()
    return render_template('main/404.html', **data), 404

def page_not_found(e):
    data = get_base_data()
    return render_template('main/404.html', **data), 404
    # return '404 page', 404

def handle_bad_request(e):
    return 'bad request!', 400

def handle_forbidden(e):
    # return 'request forbidden', 403
    return render_template('blog_admin/403.html', msg=e.description), 403

def handle_unauthorized(e):
    # return 'request forbidden', 403
    return render_template('blog_admin/401.html'), 401

def admin_page_not_found(e):
    # return render_template('404.html'), 404
    # return 'admin 404 page', 404
    return render_template('blog_admin/404.html'), 404