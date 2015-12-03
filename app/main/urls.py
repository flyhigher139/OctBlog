from flask import Blueprint

from . import views, admin_views, errors

main = Blueprint('main', __name__)

main.add_url_rule('/', 'index', views.list_posts)
main.add_url_rule('/posts/', 'posts', views.list_posts)
main.add_url_rule('/posts/<slug>/', 'post_detail', views.post_detail)
main.add_url_rule('/post/<slug>/', 'post_detail_fix', views.post_detail, defaults={'fix':True})
main.add_url_rule('/pages/<slug>/', 'page_detail', views.post_detail, defaults={'post_type':'page'})
main.add_url_rule('/archive/', 'archive', views.archive)
main.add_url_rule('/atom/', 'recent_feed', views.recent_feed)
main.add_url_rule('/sitemap.xml/', 'sitemap', views.sitemap)
main.errorhandler(404)(errors.page_not_found)
main.add_url_rule('/<path:invalid_path>', 'handle_unmatchable', errors.handle_unmatchable)


blog_admin = Blueprint('blog_admin', __name__)

blog_admin.add_url_rule('/', view_func=admin_views.AdminIndex.as_view('index'))
blog_admin.add_url_rule('/posts/', view_func=admin_views.PostsList.as_view('posts'))
blog_admin.add_url_rule('/new-post/', view_func=admin_views.Post.as_view('new_post'))
blog_admin.add_url_rule('/pages/', view_func=admin_views.PostsList.as_view('pages'), defaults={'post_type':'page'})
blog_admin.add_url_rule('/new-page/', view_func=admin_views.Post.as_view('new_page'), defaults={'post_type':'page'})
blog_admin.add_url_rule('/posts/<slug>/', view_func=admin_views.Post.as_view('edit_post'))

blog_admin.add_url_rule('/su/posts/', view_func=admin_views.SuPostsList.as_view('su_posts'))
blog_admin.add_url_rule('/su/posts/<slug>/', view_func=admin_views.SuPost.as_view('su_post_edit'))
blog_admin.errorhandler(404)(errors.admin_page_not_found)
blog_admin.errorhandler(401)(errors.handle_unauthorized)
blog_admin.errorhandler(403)(errors.handle_forbidden)