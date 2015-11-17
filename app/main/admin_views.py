from flask import request, redirect, render_template, url_for, abort, flash, g
from flask.views import MethodView
from flask.ext.login import current_user, login_required

from . import models, forms
from accounts.models import User
from accounts.permissions import admin_permission, editor_permission, writer_permission, reader_permission
from OctBlog.config import OctBlogSettings

POST_TYPES = ('post', 'page')
PER_PAGE = OctBlogSettings['pagination'].get('admin_per_page', 10)

def get_current_user(): 
    user = User.objects.get(username=current_user.get_id())
    return user

class AdminIndex(MethodView):
    decorators = [login_required]
    template_name = 'blog_admin/index.html'

    def get(self):
        blog_meta = OctBlogSettings['blog_meta']
        return render_template(self.template_name, blog_meta=blog_meta)

class PostsList(MethodView):
    decorators = [login_required]
    template_name = 'blog_admin/posts.html'
    
    def get(self, post_type='post'):
        # posts = models.Post.objects.filter(post_type=post_type)
        posts = models.Post.objects.filter(post_type=post_type).order_by('-update_time')
        if request.args.get('draft'):
            posts = posts.filter(is_draft=True)
        else:
            posts = posts.filter(is_draft=False)

        cur_page = request.args.get('page', 1)
        if not cur_page:
            abort(404)
        posts = posts.paginate(page=int(cur_page), per_page=PER_PAGE)

        return render_template(self.template_name, posts=posts, post_type=post_type)

class Post(MethodView):
    decorators = [login_required, writer_permission.require(401)]
    template_name = 'blog_admin/post.html'

    def get_context(self, slug=None, form=None, post_type='post'):
        edit_flag = slug is not None or False
        post = None

        if edit_flag:
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

        categories = models.Post.objects.distinct('category')
        tags = models.Post.objects.distinct('tags')
        
        context = {'edit_flag':edit_flag, 'form':form, 'display_slug':display_slug, 
            'categories':categories, 'tags':tags
        }

        return context

    def get(self, slug=None, form=None, post_type='post'):
        context = self.get_context(slug, form, post_type)
        return render_template(self.template_name, **context)

        # with admin_permission.require(401):
        #     context = self.get_context(slug, form, post_type)
        #     return render_template(self.template_name, **context)

    def post(self, slug=None, post_type='post'):
        form = forms.PostForm(obj=request.form)
        if not form.validate():
            return self.get(slug, form)

        if slug:
            post = models.Post.objects.get_or_404(slug=slug)
        else:
            post = models.Post()
            post.author = get_current_user()

        post.title = form.title.data.strip()
        post.slug = form.slug.data.strip()
        post.raw = form.raw.data.strip()
        abstract = form.abstract.data.strip()
        post.abstract = abstract if abstract else post.raw[:140]
        post.category = form.category.data.strip() if form.category.data.strip() else None
        post.tags = [tag.strip() for tag in form.tags_str.data.split(',')] if form.tags_str.data else None
        post.post_type = form.post_type.data if form.post_type.data else None

        redirect_url = url_for('blog_admin.pages') if form.post_type.data == 'page' else url_for('blog_admin.posts')

        if request.form.get('publish'):
            post.is_draft = False
            post.save()
            flash('Succeed to publish the {0}'.format(post_type), 'success')
            return redirect(redirect_url)

        elif request.form.get('draft'):
            post.is_draft = True
            post.save()
            flash('Succeed to save the draft', 'success')
            return redirect('{0}?draft=true'.format(redirect_url))


        return self.get(slug, form)

    def delete(self, slug):
        post = models.Post.objects.get_or_404(slug=slug)
        post_type = post.post_type
        is_draft = post.is_draft
        post.delete()

        redirect_url = url_for('blog_admin.pages') if post_type == 'page' else url_for('blog_admin.posts')
        if is_draft:
            redirect_url = redirect_url + '?draft=true'


        flash('Succeed to delete the {0}'.format(post_type), 'success')

        if request.args.get('ajax'):
            return 'success'
            
        return redirect(redirect_url)

class SuPostsList(MethodView):
    decorators = [login_required, admin_permission.require(401)]
    template_name = 'blog_admin/su_posts.html'
    
    def get(self, post_type='post'):
        # posts = models.Post.objects.filter(post_type=post_type)
        posts = models.Post.objects.all()
        # if request.args.get('draft'):
        #     posts = posts.filter(is_draft=True)
        # else:
        #     posts = posts.filter(is_draft=False)

        return render_template(self.template_name, posts=posts)

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
        
        context = {'form':form, 'display_slug':slug, 
            'categories':categories, 'tags':tags, 'post_types': POST_TYPES
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
        post.raw = form.raw.data.strip()
        abstract = form.abstract.data.strip()
        post.abstract = abstract if abstract else post.raw[:140]
        post.is_draft = form.is_draft.data
        post.author = form.author.data

        post.post_type = form.post_type.data if form.post_type.data else None

        redirect_url = url_for('blog_admin.su_posts')

        post.save()
        flash('Succeed to update post', 'success')
        return redirect(redirect_url)


