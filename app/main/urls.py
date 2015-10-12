from flask import Blueprint

from . import views

main = Blueprint('main', __name__)

main.add_url_rule('/test/', 'test', views.test)
main.add_url_rule('/', 'index', views.list_posts)
main.add_url_rule('/posts/', 'posts', views.list_posts)
main.add_url_rule('/posts/<slug>/', 'post_detail', views.post_detail)


blog_admin = Blueprint('blog_admin', __name__)

blog_admin.add_url_rule('/', view_func=views.AdminIndex.as_view('admin_index'))