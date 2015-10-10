from flask import Blueprint

from . import views

main = Blueprint('main', __name__)

main.add_url_rule('/test/', 'test', views.test)
main.add_url_rule('/', 'index', views.index)
main.add_url_rule('/posts/', 'posts', views.list_posts)
main.add_url_rule('/posts/<slug>/', 'post_detail', views.post_detail)