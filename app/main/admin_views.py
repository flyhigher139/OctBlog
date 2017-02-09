#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, datetime, random, json, re, os

from flask import request, redirect, render_template, url_for, abort, flash, g, current_app, send_from_directory
from flask.views import MethodView
# from flask.ext.login import current_user, login_required
from flask_login import current_user, login_required
import dateutil.parser

from . import models, forms, signals
from accounts.models import User
from accounts.permissions import admin_permission, editor_permission, writer_permission, reader_permission
from OctBlog.config import OctBlogSettings

POST_TYPES = models.POST_TYPE_CHOICES
# POST_TYPES = OctBlogSettings['post_types']
PER_PAGE = OctBlogSettings['pagination'].get('admin_per_page', 10)

article_models = {
    'post': models.Post,
    'draft': models.Draft
}

# post_urls = {
#     'post': url_for('blog_admin.posts'),
#     'page': url_for('blog_admin.pages'),
#     'wechat': url_for('blog_admin.wechats'),
# }

# draft_urls = {
#     'post': url_for('blog_admin.drafts'),
#     'page': url_for('blog_admin.page_drafts'),
#     'wechat': url_for('blog_admin.wechat_drafts'),
# }

def get_current_user(): 
    user = User.objects.get(username=current_user.get_id())
    return user

class AdminIndex(MethodView):
    decorators = [login_required]
    template_name = 'blog_admin/index.html'

    def get(self):
        blog_meta = OctBlogSettings['blog_meta']
        user = get_current_user()
        return render_template(self.template_name, blog_meta=blog_meta, user=user)

class PostsList(MethodView):
    decorators = [login_required]
    template_name = 'blog_admin/posts.html'
    is_draft = False
    article_model = models.Post
    
    def get(self, post_type='post'):
        posts = self.article_model.objects.filter(post_type=post_type).order_by('-update_time')

        if not g.identity.can(editor_permission):
            posts = posts.filter(author=get_current_user())

        try:
            cur_page = int(request.args.get('page', 1))
        except:
            cur_page = 1

        posts = posts.paginate(page=cur_page, per_page=PER_PAGE)

        return render_template(self.template_name, posts=posts, post_type=post_type, is_draft=self.is_draft)

class DraftList(PostsList):
    is_draft = True
    article_model = models.Draft

class PostStatisticList(MethodView):
    decorators = [login_required, editor_permission.require(401)]
    template_name = 'blog_admin/post_statistics.html'
    
    def get(self):
        posts = models.PostStatistics.objects.all()

        try:
            cur_page = int(request.args.get('page', 1))
        except:
            cur_page = 1

        posts = posts.paginate(page=cur_page, per_page=PER_PAGE*2)

        return render_template(self.template_name, posts=posts)

class PostStatisticDetail(MethodView):
    decorators = [login_required, editor_permission.require(401)]
    template_name = 'blog_admin/post_statistics_detail.html'

    def get(self, slug):
        post = models.Post.objects.get_or_404(slug=slug)
        post_statistics = models.PostStatistics.objects.get_or_404(post=post)
        trackers = models.Tracker.objects(post=post)

        try:
            cur_page = int(request.args.get('page', 1))
        except:
            cur_page = 1

        trackers = trackers.paginate(page=cur_page, per_page=PER_PAGE*2)

        data = {'post_statistics':post_statistics, 'trackers':trackers, 'post':post }

        return render_template(self.template_name, **data)

class Post(MethodView):
    decorators = [login_required, writer_permission.require(401)]
    template_name = 'blog_admin/post.html'

    def get(self, slug=None, form=None, post_type='post', is_draft=False):
        edit_flag = slug is not None or False
        post = None

        if edit_flag:
            try:
                post = models.Draft.objects.get(slug=slug)
                post.from_draft = 'true'
            except models.Draft.DoesNotExist:
                post = models.Post.objects.get_or_404(slug=slug)

            if not g.identity.can(editor_permission) and post.author.username != current_user.username:
                abort(401)

        display_slug = slug if slug else 'slug-value'

        if not form:
            if post:
                # post = models.Post.objects.get_or_404(slug=slug)
                post.post_id = str(post.id)
                post.tags_str = ', '.join(post.tags)
                form = forms.PostForm(obj=post)
            else:
                form = forms.PostForm(post_type=post_type)

        categories = models.Post.objects(post_type=post_type).distinct('category')
        tags = models.Post.objects(post_type=post_type).distinct('tags')
        
        context = {'edit_flag':edit_flag, 'form':form, 'display_slug':display_slug, 
            'categories':categories, 'tags':tags
        }

        # return context
        return render_template(self.template_name, **context)



    def post(self, slug=None, post_type='post', is_draft=False):
        article_model = article_models['post'] if request.form.get('publish') else article_models['draft']

        form = forms.PostForm(obj=request.form)
        if not form.validate():
            return self.get(slug, form)

        # if slug:
        #     post = article_model.objects.get_or_404(slug=slug)
        # else:
        #     post = article_model()
        #     post.author = get_current_user()

        try:
            post = article_model.objects.get_or_404(slug=slug)
        except:
            post = article_model()
            post.author = get_current_user()

        post.title = form.title.data.strip()
        post.slug = form.slug.data.strip()
        post.raw = form.raw.data.strip()
        abstract = form.abstract.data.strip()
        post.abstract = abstract if abstract else post.raw[:140]
        post.category = form.category.data.strip() if form.category.data.strip() else None
        post.tags = [tag.strip() for tag in form.tags_str.data.split(',')] if form.tags_str.data else None
        post.post_type = form.post_type.data if form.post_type.data else None


        post_urls = {
            'post': url_for('blog_admin.posts'),
            'page': url_for('blog_admin.pages'),
            'wechat': url_for('blog_admin.wechats'),
        }

        draft_urls = {
            'post': url_for('blog_admin.drafts'),
            'page': url_for('blog_admin.page_drafts'),
            'wechat': url_for('blog_admin.wechat_drafts'),
        }

        

        if request.form.get('publish'):
            post.is_draft = False
            msg = 'Succeed to publish the {0}'.format(post_type)
            # redirect_url = url_for('blog_admin.pages') if form.post_type.data == 'page' else url_for('blog_admin.posts')
            redirect_url = post_urls[form.post_type.data]
            post.save()

            signals.post_pubished.send(current_app._get_current_object(), post=post)

            try:
                draft = models.Draft.objects.get(slug=slug)
                draft.delete()
            except:
                pass

            try:
                post_statistic = models.PostStatistics.objects.get(post=post)
            except models.PostStatistics.DoesNotExist:
                post_statistic = models.PostStatistics()
                post_statistic.post = post
                post_statistic.verbose_count_base = random.randint(500, 5000)
                post_statistic.save()

        elif request.form.get('draft'):
            post.is_draft = True
            msg = 'Succeed to save the draft'
            # redirect_url = url_for('blog_admin.page_drafts') if form.post_type.data == 'page' else url_for('blog_admin.drafts')
            redirect_url = draft_urls[form.post_type.data]
            post.save()
        else:
            return self.get(slug, form, is_draft)

        

        flash(msg, 'success')
        return redirect(redirect_url)


    def delete(self, slug):
        if request.args.get('is_draft') and request.args.get('is_draft').lower()=='true':
            article_model = article_models['draft']
        else:
            article_model = article_models['post']
        post = article_model.objects.get_or_404(slug=slug)
        post_type = post.post_type
        # is_draft = post.is_draft

        try:
            post_statistic = models.PostStatistics.objects.get(post=post)
            post_statistic.delete()
        except:
            pass
            
        post.delete()

        redirect_url = url_for('blog_admin.pages') if post_type == 'page' else url_for('blog_admin.posts')
        # if is_draft:
        #     redirect_url = redirect_url + '?draft=true'


        flash('Succeed to delete the {0}'.format(post_type), 'success')

        if request.args.get('ajax'):
            return 'success'
            
        return redirect(redirect_url)

class SuPostsList(MethodView):
    decorators = [login_required, admin_permission.require(401)]
    template_name = 'blog_admin/su_posts.html'
    
    def get(self):
        posts = models.Post.objects.all().order_by('-update_time')
        cur_type = request.args.get('type')
        # post_types = posts.distinct('post_type')
        if cur_type:
            posts = posts.filter(post_type=cur_type)

        cur_page = request.args.get('page', 1)
        if not cur_page:
            abort(404)
        posts = posts.paginate(page=int(cur_page), per_page=PER_PAGE)

        data = {
            'posts':posts,
            'post_types': POST_TYPES,
            'cur_type': cur_type
        }

        return render_template(self.template_name, **data)

class SuPost(MethodView):
    decorators = [login_required, admin_permission.require(401)]
    template_name = 'blog_admin/su_post.html'

    def get_context(self, slug, form=None):
        post = models.Post.objects.get_or_404(slug=slug)

        if not form:
            # post.post_id = str(post.id)
            # post.tags_str = ', '.join(post.tags)
            form = forms.SuPostForm(obj=post)

        categories = models.Post.objects.distinct('category')
        tags = models.Post.objects.distinct('tags')
        
        context = {'form':form, 'display_slug':slug, 'post': post,
            'categories':categories, 'tags':tags, 'post_types': POST_TYPES, 
        }

        return context

    def get(self, slug, form=None):
        context = self.get_context(slug, form)
        return render_template(self.template_name, **context)

    def post(self, slug):
        form = forms.SuPostForm(request.form)
        if not form.validate():
            return self.get(slug, form)

        # return form.author.data.username

        # if slug:
        #     post = models.Post.objects.get_or_404(slug=slug)
        # else:
        #     post = models.Post()
        #     post.author = get_current_user()

        post = models.Post.objects.get_or_404(slug=slug)

        post.title = form.title.data.strip()
        post.slug = form.slug.data.strip()
        post.fix_slug = form.fix_slug.data.strip()
        post.raw = form.raw.data.strip()
        abstract = form.abstract.data.strip()
        post.abstract = abstract if abstract else post.raw[:140]
        post.is_draft = form.is_draft.data
        post.author = form.author.data

        # post.post_type = form.post_type.data.strip() if form.post_type.data else None

        post.post_type = request.form.get('post_type') or post.post_type
        pub_time = request.form.get('publish_time')
        update_time = request.form.get('update_time')

        if pub_time:
            post.pub_time = datetime.datetime.strptime(pub_time, "%Y-%m-%d %H:%M:%S")

        if update_time:
            post.update_time = datetime.datetime.strptime(update_time, "%Y-%m-%d %H:%M:%S")

        redirect_url = url_for('blog_admin.su_posts')

        post.save(allow_set_time=True)

        flash('Succeed to update post', 'success')
        return redirect(redirect_url)

class WidgetList(MethodView):
    decorators = [login_required, admin_permission.require(401)]
    template_name = 'blog_admin/widgets.html'
    
    def get(self):
        widgets = models.Widget.objects.all()
        data = {
            'widgets':widgets, 
        }

        return render_template(self.template_name, **data)

class Widget(MethodView):
    decorators = [login_required, admin_permission.require(401)]
    template_name = 'blog_admin/widget.html'

    def get(self, pk=None, form=None):
        widget = None
        if pk:
            widget = models.Widget.objects.get_or_404(id=pk)
            if widget.md_content:
                widget.content = widget.md_content
                widget.content_type = 'markdown'
            else:
                widget.content = widget.html_content
                widget.content_type = 'html'

        if not form:
            if pk:
                form = forms.WidgetForm(obj=widget)
            else:
                form = forms.WidgetForm()

        data = {'form':form, 'widget':widget, 'post_types': POST_TYPES,}
        return render_template(self.template_name, **data)

    def post(self, pk=None, form=None):
        form = forms.WidgetForm(request.form)
        if not form.validate():
            return self.get(pk, form)


        if pk:
            widget = models.Widget.objects.get_or_404(id=pk)
        else:
            widget = models.Widget()

        widget.title = form.title.data.strip()
        if form.content_type.data == 'html':
            widget.html_content = form.content.data.strip()
            widget.md_content = None
        else:
            widget.md_content = form.content.data.strip()

        widget.priority = form.priority.data

        allow_post_types = request.form.get('allow_post_types').split(',')
        widget.allow_post_types = [post_type.strip() for post_type in allow_post_types]
        
        update_time = request.form.get('update_time')
        if update_time:
            widget.update_time = update_time

        widget.save()

        msg1 = 'Succeed to create widget'
        msg2 = 'Succeed to update widget'
        msg = msg1 if pk else msg2
        flash(msg, 'success')

        return redirect(url_for('blog_admin.su_widgets'))


    def delete(self, pk):
        widget = models.Widget.objects.get_or_404(id=pk)
        widget.delete()

        if request.args.get('ajax'):
            return 'success'

        redirect_url = url_for('blog_admin.su_widgets')


        flash('Succeed to delete the widget', 'success')
            
        return redirect(redirect_url)

class Comment(MethodView):
    decorators = [login_required, editor_permission.require(401)]
    template_name = 'blog_admin/comments.html'
    def get(self, status='pending', pk=None):
        if pk:
            return redirect(url_for('blog_admin.comments'))
            
        data = {}
        comments = models.Comment.objects(status=status)

        keyword = request.args.get('keyword')
        if keyword:
            comments = comments.filter(md_content__icontains=keyword)

        try:
            cur_page = int(request.args.get('page', 1))
        except:
            cur_page = 1
        comments = comments.paginate(page=cur_page, per_page=10)

        data['status'] = status
        data['comments'] = comments
        data['keyword'] = keyword

        return render_template(self.template_name, **data)

    def put(self, pk):
        comment = models.Comment.objects.get_or_404(pk=pk)
        comment.status = 'approved'
        comment.save()

        if request.args.get('ajax'):
            return 'success'

        msg = 'The comment has been approved'
        flask(msg, 'success')
        return redirect(url_for('blog_admin.comments_approved'))

    def delete(self, pk):
        comment = models.Comment.objects.get_or_404(pk=pk)
        comment.delete()

        if request.args.get('ajax'):
            return 'success'

        msg = 'The comment has been deleted'
        flask(msg, 'success')
        return redirect(url_for('blog_admin.comments_approved'))

class ImportCommentView(MethodView):
    decorators = [login_required, editor_permission.require(401)]
    template_name = 'blog_admin/import_comments.html'

    def get(self, form=None):
        if not form:
            form = forms.ImportCommentForm()
        data = {'form': form}
        return render_template(self.template_name, **data)

    def post(self):
        form = forms.ImportCommentForm(obj=request.form)
        if not form.validate():
            return self.get(form=form)

        if form.json_file.data and form.import_format.data=='file':
            msg = 'Import from file is not ready yet'
            flash(msg, 'warning')
            return redirect(url_for('blog_admin.import_comments'))

        try:
            comment_json = json.loads(form.content.data)
        except:
            msg = 'Json data error'
            flash(msg, 'warning')
            return redirect(url_for('blog_admin.import_comments'))

        url_regx = re.compile('^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$')
        def clean_url(url):
            if not url:
                return None
            url = url.replace('\\', '')
            clean = url_regx.match(url)
            if not clean:
                # print url
                return None

            return url


        imported_comments = comment_json['posts']
        for import_comment in imported_comments:
            comment = models.Comment()
            comment.author = import_comment['author_name']
            comment.email = import_comment['author_email']
            comment.homepage = clean_url(import_comment['author_url'])
            comment.post_slug = import_comment['thread_key']
            comment.post_title = import_comment['thread_key']
            comment.md_content = import_comment['message']
            comment.pub_time = dateutil.parser.parse(import_comment['created_at'])
            comment.update_time = dateutil.parser.parse(import_comment['updated_at'])
            comment.status = 'approved'
            comment.misc = 'duoshuo'

            comment.save()

        msg = 'Succeed to import comments'
        flash(msg, 'success')
        return redirect(url_for('blog_admin.comments_approved'))

class SuExportView(MethodView):
    template_name = 'blog_admin/su_export.html'

    def get(self):
        return render_template(self.template_name)

    def post(self):
        obj_type = request.form.get('type')
        obj_format = request.form.get('format')

        export_methods = {
            'Posts':{
                'json':self.export_posts_json,
                'zip': self.export_posts_zip
            },
            'Comments':{
                'json':self.export_comments_json,
                'zip': self.export_comments_zip
            }
        }

        return export_methods[obj_type][obj_format]()
        # export_path, file_name = export_methods[obj_type][obj_format]()
        # return export_path+file_name

        # return 'Type: {0}, Format: {1}'.format(obj_type, obj_format)
        # return 'Not ready yet'

    def export_posts_json(self):
        posts = models.Post.objects()
        post_list = [post.to_dict() for post in posts]

        export_path = current_app._get_current_object().config['EXPORT_PATH']
        file_name = 'all_posts.json'
        file_fullname = os.path.join(export_path, file_name)

        with open(file_fullname, 'w') as fs:
            json.dump(post_list, fs, ensure_ascii=True)

        return send_from_directory(export_path, file_name, as_attachment=True)

        return 'Succeed to export posts'
        return (export_path, file_name)

    def export_posts_zip(self):
        return 'Not ready yet'

    def export_comments_json(self):
        return 'Not ready yet'

    def export_comments_zip(self):
        return 'Not ready yet'