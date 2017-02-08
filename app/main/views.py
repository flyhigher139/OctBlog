#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urlparse import urljoin
from datetime import datetime, timedelta

from flask import request, redirect, render_template, url_for, abort, flash, g, session
from flask import current_app, make_response
from flask.views import MethodView

# from flask.ext.login import login_required, current_user
from flask_login import login_required, current_user

from werkzeug.contrib.atom import AtomFeed
from mongoengine.queryset.visitor import Q


from . import models, signals, forms
from accounts.models import User
from accounts.permissions import admin_permission, editor_permission, writer_permission, reader_permission
from OctBlog.config import OctBlogSettings


PER_PAGE = OctBlogSettings['pagination'].get('per_page', 10)
ARCHIVE_PER_PAGE = OctBlogSettings['pagination'].get('archive_per_page', 10)


def get_base_data():
    pages = models.Post.objects.filter(post_type='page', is_draft=False)
    blog_meta = OctBlogSettings['blog_meta']
    data = {'blog_meta':blog_meta, 'pages':pages}
    return data

def index():
    return 'Hello'

def list_posts():
    posts = models.Post.objects.filter(post_type='post', is_draft=False).order_by('-pub_time')

    tags = posts.distinct('tags')

    try:
        cur_page = int(request.args.get('page', 1))
    except ValueError:
        cur_page = 1


    cur_category = request.args.get('category')
    cur_tag = request.args.get('tag')
    keywords = request.args.get('keywords')


    if keywords:
        # posts = posts.filter(raw__contains=keywords )
        posts = posts.filter(Q(raw__contains=keywords) | Q(title__contains=keywords))

    if cur_category:
        posts = posts.filter(category=cur_category)

    if cur_tag:
        posts = posts.filter(tags=cur_tag)


    #group by aggregate
    category_cursor = models.Post._get_collection().aggregate([
            { '$group' :
                { '_id' : {'category' : '$category' },
                  'name' : { '$first' : '$category' },
                  'count' : { '$sum' : 1 },
                }
            }
        ])

    widgets = models.Widget.objects(allow_post_types='post')




    posts = posts.paginate(page=cur_page, per_page=PER_PAGE)

    data = get_base_data()
    data['posts'] = posts
    data['cur_category'] = cur_category
    data['category_cursor'] = category_cursor
    data['cur_tag'] = cur_tag
    data['tags'] = tags
    data['keywords'] = keywords
    data['widgets'] = widgets

    return render_template('main/index.html', **data)

def list_wechats():
    posts = models.Post.objects.filter(post_type='wechat', is_draft=False).order_by('-pub_time')

    tags = posts.distinct('tags')

    try:
        cur_page = int(request.args.get('page', 1))
    except ValueError:
        cur_page = 1


    cur_tag = request.args.get('tag')
    keywords = request.args.get('keywords')


    if keywords:
        # posts = posts.filter(raw__contains=keywords )
        posts = posts.filter(Q(raw__contains=keywords) | Q(title__contains=keywords))


    if cur_tag:
        posts = posts.filter(tags=cur_tag)


    posts = posts.paginate(page=cur_page, per_page=PER_PAGE)

    widgets = models.Widget.objects(allow_post_types='wechat')

    data = get_base_data()
    data['posts'] = posts
    data['cur_tag'] = cur_tag
    data['tags'] = tags
    data['keywords'] = keywords
    data['widgets'] = widgets

    return render_template('main/wechat_list.html', **data)

def post_detail(slug, post_type='post', fix=False, is_preview=False):
    if is_preview:
        if not g.identity.can(reader_permission):
            abort(401)
        post = models.Draft.objects.get_or_404(slug=slug, post_type=post_type)
    else:
        post = models.Post.objects.get_or_404(slug=slug, post_type=post_type) if not fix else models.Post.objects.get_or_404(fix_slug=slug, post_type=post_type)

    # this block is abandoned
    if post.is_draft and current_user.is_anonymous:
        abort(404)

    data = get_base_data()
    data['post'] = post
    data['post_type'] = post_type

    if request.form:
        form = forms.CommentForm(obj=request.form)
    else:
        obj = {'author': session.get('author'), 'email': session.get('email'),'homepage': session.get('homepage'),}
        form = forms.CommentForm(**obj)
        # print session.get('email')


    if request.form.get('oct-comment') and form.validate_on_submit():
        octblog_create_comment(form, post)
        url = '{0}#comment'.format(url_for('main.post_detail', slug=slug))
        msg = 'Succeed to comment, and it will be displayed when the administrator reviews it.'
        flash(msg, 'success')
        return redirect(url)

    data['allow_donate'] = OctBlogSettings['donation']['allow_donate']
    data['donation_msg'] = OctBlogSettings['donation']['donation_msg']

    data['display_wechat'] = OctBlogSettings['wechat']['display_wechat']
    data['wechat_msg'] = OctBlogSettings['wechat']['wechat_msg']

    data['display_copyright'] = OctBlogSettings['copyright']['display_copyright']
    data['copyright_msg'] = OctBlogSettings['copyright']['copyright_msg']

    data['allow_comment'] = OctBlogSettings['blog_comment']['allow_comment']
    if data['allow_comment']:
        comment_type = OctBlogSettings['blog_comment']['comment_type']
        comment_shortname = OctBlogSettings['blog_comment']['comment_opt'][comment_type]
        comment_func = get_comment_func(comment_type)
        data['comment_html'] = comment_func(slug, post.title, request.base_url, comment_shortname, form=form) if comment_func else ''

    data['allow_share_article'] = OctBlogSettings['allow_share_article']
    # if data['allow_share_article']:
    #     data['share_html'] = jiathis_share()

    # send signal
    if not is_preview:
        signals.post_visited.send(current_app._get_current_object(), post=post)

    templates = {
        'post': 'main/post.html',
        'page': 'main/post.html',
        'wechat': 'main/wechat_detail.html',
    }

    return render_template(templates[post_type], **data)

def post_preview(slug, post_type='post'):
    return post_detail(slug=slug, post_type=post_type, is_preview=True)

def post_detail_general(slug, post_type):
    is_preview = request.args.get('is_preview', 'false')
    is_preview = True if is_preview.lower()=='true' else False
    return post_detail(slug=slug, post_type=post_type, is_preview=is_preview)

def author_detail(username):
    author = User.objects.get_or_404(username=username)

    posts = models.Post.objects.filter(post_type='post', is_draft=False, author=author).order_by('-pub_time')
    cur_page = request.args.get('page', 1)

    posts = posts.paginate(page=int(cur_page), per_page=ARCHIVE_PER_PAGE)

    data = get_base_data()
    data['user'] = author
    data['posts'] = posts
    # data['category_cursor'] = category_cursor
    # data['cur_tag'] = cur_tag
    # data['tags'] = tags
    # data['keywords'] = keywords

    return render_template('main/author.html', **data)


def get_comment_func(comment_type):
    # if comment_type == 'duoshuo':
    #     return duoshuo_comment
    # else:
    #     return None
    comment_func = {
        'octblog': octblog_comment,
        'duoshuo': duoshuo_comment,
    }

    return comment_func.get(comment_type)

def octblog_comment(post_id, post_title, post_url, comment_shortname, form=None, *args, **kwargs):
    template_name = 'main/comments.html'
    comments = models.Comment.objects(post_slug=post_id, status='approved').order_by('pub_time')
    # print comments[0].get_gavatar_url()
    # if not form:
    #     if session.get('author'):
    #         print 'session'
    #         return 'session'
    #         data = {'author': session['author'], 'email': session['email'],'homepage': session['homepage'],}
    #         form = forms.SessionCommentForm(obj=data)
    #     else:
    #         print 'no session'
    #         return 'no session'
    #         form = forms.CommentForm(obj=request.form)
    data = {
        'form': form,
        'comments': comments,
        'slug': post_id,
    }
    return render_template(template_name, **data)

def octblog_create_comment(form, post):
    comment = models.Comment()
    comment.author = form.author.data.strip()
    comment.email = form.email.data.strip()
    comment.homepage = form.homepage.data.strip() or None
    comment.post_slug = post.slug
    comment.post_title = post.title
    comment.md_content = form.content.data.strip()
    comment.save()

    session['author'] = form.author.data.strip()
    session['email'] = form.email.data.strip()
    session['homepage'] = form.homepage.data.strip()


def duoshuo_comment(post_id, post_title, post_url, duoshuo_shortname, *args, **kwargs):
    '''
    Create duoshuo script by params
    '''
    template_name = 'main/misc/duoshuo.html'
    data = {
        'duoshuo_shortname': duoshuo_shortname,
        'post_id': post_id,
        'post_title': post_title,
        'post_url': post_url,
    }

    return render_template(template_name, **data)

# def jiathis_share():
#     '''
#     Create duoshuo script by params
#     '''
#     template_name = 'main/misc/jiathis_share.html'

#     return render_template(template_name)

def archive():
    posts = models.Post.objects.filter(post_type='post', is_draft=False).order_by('-pub_time')

    cur_category = request.args.get('category')
    cur_tag = request.args.get('tag')
    cur_page = request.args.get('page', 1)

    if cur_category:
        posts = posts.filter(category=cur_category)

    if cur_tag:
        posts = posts.filter(tags=cur_tag)

    posts = posts.paginate(page=int(cur_page), per_page=ARCHIVE_PER_PAGE)

    data = get_base_data()
    data['posts'] = posts

    return render_template('main/archive.html', **data)

def make_external(url):
    return urljoin(request.url_root, url)

def get_post_footer(allow_donate=False, donation_msg=None,
                    display_wechat=False, wechat_msg=None,
                    display_copyright=False, copyright_msg=None, *args, **kwargs):
    template_name = 'main/misc/post_footer.html'
    data = {}
    data['allow_donate'] = allow_donate
    data['donation_msg'] = donation_msg

    data['display_wechat'] = display_wechat
    data['wechat_msg'] = wechat_msg

    data['display_copyright'] = display_copyright
    data['copyright_msg'] = copyright_msg

    return render_template(template_name, **data)

def recent_feed():
    feed_title = OctBlogSettings['blog_meta']['name']
    feed = AtomFeed(feed_title, feed_url=request.url, url=request.url_root)

    # data = {}
    # data['allow_donate'] = OctBlogSettings['donation']['allow_donate']
    # data['donation_msg'] = OctBlogSettings['donation']['donation_msg']

    # data['display_wechat'] = OctBlogSettings['wechat']['display_wechat']
    # data['wechat_msg'] = OctBlogSettings['wechat']['wechat_msg']

    # data['display_copyright'] = OctBlogSettings['copyright']['display_copyright']
    # data['copyright_msg'] = OctBlogSettings['copyright']['copyright_msg']

    # post_footer = get_post_footer(**data)

    posts = models.Post.objects.filter(post_type='post', is_draft=False)[:15]
    only_abstract_in_feed = OctBlogSettings['only_abstract_in_feed']
    content = 'abstract' if only_abstract_in_feed else 'content_html'
    for post in posts:
        # return post.get_absolute_url()
        feed.add(post.title, 
                 # unicode(post.content_html),
                 # post.abstract,
                 getattr(post, content),
                 content_type='html',
                 author=post.author.username,
                 url=post.get_absolute_url(),
                 updated=post.update_time,
                 published=post.pub_time)
    return feed.get_response()

def sitemap():
    """Generate sitemap.xml. Makes a list of urls and date modified."""
    pages=[]

    #########################
    # static pages
    #########################

    # ten_days_ago=(datetime.now() - timedelta(days=10)).date().isoformat()

    # for rule in current_app.url_map.iter_rules():
    #     if "GET" in rule.methods and len(rule.arguments)==0:
    #         pages.append(
    #                      [rule.rule,ten_days_ago]
    #                      )

    ## user model pages
    # users=User.query.order_by(User.modified_time).all()
    # for user in users:
    #     url=url_for('user.pub',name=user.name)
    #     modified_time=user.modified_time.date().isoformat()
    #     pages.append([url,modified_time])

    ######################
    # Post Pages
    ######################

    posts = models.Post.objects.filter(is_draft=False, post_type='post')
    for post in posts:
        pages.append((post.get_absolute_url(), post.update_time.date().isoformat(), 'weekly', '0.8'))

    ######################
    # Blog-Page Pages
    ######################

    blog_pages = models.Post.objects.filter(is_draft=False, post_type='page')
    for page in blog_pages:
        pages.append((page.get_absolute_url(), page.update_time.date().isoformat(), 'monthly', '0.7'))

    ######################
    # Wechat Pages
    ######################

    posts = models.Post.objects.filter(is_draft=False, post_type='wechat')
    for post in posts:
        pages.append((post.get_absolute_url(), post.update_time.date().isoformat(), 'weekly', '0.6'))

    sitemap_xml = render_template('main/sitemap.xml', pages=pages)
    response= make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response
