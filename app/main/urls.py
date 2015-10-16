from flask import Blueprint

from . import views, admin_views

main = Blueprint('main', __name__)

main.add_url_rule('/', 'index', views.list_posts)
main.add_url_rule('/posts/', 'posts', views.list_posts)
main.add_url_rule('/posts/<slug>/', 'post_detail', views.post_detail)
main.add_url_rule('/pages/<slug>/', 'page_detail', views.post_detail, defaults={'post_type':'page'})
main.add_url_rule('/atom/', 'recent_feed', views.recent_feed)


blog_admin = Blueprint('blog_admin', __name__)

blog_admin.add_url_rule('/', view_func=admin_views.AdminIndex.as_view('index'))
blog_admin.add_url_rule('/posts/', view_func=admin_views.PostsList.as_view('posts'))
blog_admin.add_url_rule('/new-post/', view_func=admin_views.Post.as_view('new_post'))
blog_admin.add_url_rule('/pages/', view_func=admin_views.PostsList.as_view('pages'), defaults={'post_type':'page'})
blog_admin.add_url_rule('/new-page/', view_func=admin_views.Post.as_view('new_page'), defaults={'post_type':'page'})
blog_admin.add_url_rule('/posts/<slug>/', view_func=admin_views.Post.as_view('edit_post'))