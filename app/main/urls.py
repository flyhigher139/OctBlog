from flask import Blueprint

from . import views, admin_views, errors

main = Blueprint('main', __name__)

main.add_url_rule('/', 'index', views.list_posts)
main.add_url_rule('/posts/', 'posts', views.list_posts)
main.add_url_rule('/wechats/', 'wechats', views.list_wechats)
main.add_url_rule('/posts/<slug>/', 'post_detail', views.post_detail, methods=['GET', 'POST'])
main.add_url_rule('/post/<slug>/', 'post_detail_fix', views.post_detail, defaults={'fix':True})
main.add_url_rule('/posts/<slug>/preview/', 'post_preview', views.post_detail, defaults={'is_preview':True})
main.add_url_rule('/posts/<slug>/<post_type>/preview/', 'post_general_preview', views.post_detail_general)
main.add_url_rule('/pages/<slug>/', 'page_detail', views.post_detail, defaults={'post_type':'page'})
main.add_url_rule('/wechats/<slug>/', 'wechat_detail', views.post_detail, defaults={'post_type':'wechat'})
main.add_url_rule('/archive/', 'archive', views.archive)
main.add_url_rule('/users/<username>/', 'author_detail', views.author_detail)
main.add_url_rule('/atom/', 'recent_feed', views.recent_feed)
main.add_url_rule('/sitemap.xml/', 'sitemap', views.sitemap)
main.errorhandler(404)(errors.page_not_found)
main.errorhandler(401)(errors.handle_unauthorized)
main.add_url_rule('/<path:invalid_path>', 'handle_unmatchable', errors.handle_unmatchable)


blog_admin = Blueprint('blog_admin', __name__)

blog_admin.add_url_rule('/', view_func=admin_views.AdminIndex.as_view('index'))

blog_admin.add_url_rule('/posts/', view_func=admin_views.PostsList.as_view('posts'))
blog_admin.add_url_rule('/posts/draft/', view_func=admin_views.DraftList.as_view('drafts'))
blog_admin.add_url_rule('/new-post/', view_func=admin_views.Post.as_view('new_post'))
blog_admin.add_url_rule('/posts/<slug>/', view_func=admin_views.Post.as_view('edit_post'))

blog_admin.add_url_rule('/pages/', view_func=admin_views.PostsList.as_view('pages'), defaults={'post_type':'page'})
blog_admin.add_url_rule('/pages/draft/', view_func=admin_views.DraftList.as_view('page_drafts'), defaults={'post_type':'page'})
blog_admin.add_url_rule('/new-page/', view_func=admin_views.Post.as_view('new_page'), defaults={'post_type':'page'})

blog_admin.add_url_rule('/wechats/', view_func=admin_views.PostsList.as_view('wechats'), defaults={'post_type':'wechat'})
blog_admin.add_url_rule('/wechats/draft/', view_func=admin_views.DraftList.as_view('wechat_drafts'), defaults={'post_type':'wechat'})
blog_admin.add_url_rule('/new-wechat/', view_func=admin_views.Post.as_view('new_wechat'), defaults={'post_type':'wechat'})

blog_admin.add_url_rule('/posts/statistics/', view_func=admin_views.PostStatisticList.as_view('post_statistics'))
blog_admin.add_url_rule('/posts/statistics/<slug>/', view_func=admin_views.PostStatisticDetail.as_view('post_statistics_detail'))

blog_admin.add_url_rule('/posts/comments/', view_func=admin_views.Comment.as_view('comments'))
blog_admin.add_url_rule('/posts/comments/approved/', view_func=admin_views.Comment.as_view('comments_approved'), defaults={'status':'approved'})
blog_admin.add_url_rule('/posts/comments/spam/', view_func=admin_views.Comment.as_view('comments_spam'), defaults={'status':'spam'})
blog_admin.add_url_rule('/posts/comments/<pk>/action/', view_func=admin_views.Comment.as_view('comment_action'))
blog_admin.add_url_rule('/posts/comments/import/', view_func=admin_views.ImportCommentView.as_view('import_comments'))

blog_admin.add_url_rule('/su/posts/', view_func=admin_views.SuPostsList.as_view('su_posts'))
blog_admin.add_url_rule('/su/posts/<slug>/', view_func=admin_views.SuPost.as_view('su_post_edit'))
blog_admin.add_url_rule('/su/widgets/', view_func=admin_views.WidgetList.as_view('su_widgets'))
blog_admin.add_url_rule('/su/widgets/create/', view_func=admin_views.Widget.as_view('su_widget'))
blog_admin.add_url_rule('/su/widgets/<pk>/', view_func=admin_views.Widget.as_view('su_widget_edit'))
blog_admin.add_url_rule('/su/export/', view_func=admin_views.SuExportView.as_view('su_export'))

blog_admin.errorhandler(404)(errors.admin_page_not_found)
blog_admin.errorhandler(401)(errors.handle_unauthorized)
blog_admin.errorhandler(403)(errors.handle_forbidden)

