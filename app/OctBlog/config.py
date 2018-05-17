#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os, sys, datetime

def get_env_value(key, default_value=''):
    if sys.version_info < (3, 0):
        return os.environ.get(key, default_value).decode('utf8')
    else:
        return os.environ.get(key, default_value)

OctBlogSettings = {
    'post_types': ('post', 'page'), # deprecated
    'allow_registration': os.environ.get('allow_registration', 'false').lower() == 'true',
    'allow_su_creation': os.environ.get('allow_su_creation', 'false').lower() == 'true',
    'allow_donate': os.environ.get('allow_donate', 'true').lower() == 'true',
    'auto_role': os.environ.get('auto_role', 'reader').lower(),
    'blog_meta': {
        'name': get_env_value('name', 'Oct Blog'),
        'subtitle': get_env_value('subtitle', 'Oct Blog Subtitle'),
        'description': get_env_value('description', 'Oct Blog Description'),
        'wechat_name': get_env_value('wechat_name', 'Oct Blog Wechat Root'),
        'wechat_subtitle': get_env_value('wechat_subtitle', 'Oct Blog Wechat Subtitle'),
        'owner': get_env_value('owner', 'Gevin'),
        'keywords': get_env_value('keywords', 'python,django,flask,docker,MongoDB'),
        'google_site_verification': os.environ.get('google_site_verification') or '12345678',
        'baidu_site_verification': os.environ.get('baidu_site_verification') or '87654321',
        'sogou_site_verification': os.environ.get('sogou_site_verification') or '87654321',
    },
    'search_engine_submit_urls':{
        'baidu': os.environ.get('baidu_submit_url')
    },
    'pagination':{
        'per_page': int(os.environ.get('per_page', 5)),
        'admin_per_page': int(os.environ.get('admin_per_page', 10)),
        'archive_per_page': int(os.environ.get('archive_per_page', 20)),
    },
    'blog_comment':{
        'allow_comment': os.environ.get('allow_comment', 'true').lower() == 'true',
        'comment_type': os.environ.get('comment_type', 'octblog').lower(), # currently, OctBlog only supports duoshuo comment
        'comment_opt':{
            'octblog': 'oct-blog', # shotname of octblog
            'duoshuo': 'oct-blog', # shotname of duoshuo
            }
    },
    'donation': {
        'allow_donate': os.environ.get('allow_donate', 'true').lower() == 'true',
        'donation_msg': get_env_value('donation_msg', 'You can donate to me if the article makes sense to you'),
        'donation_img_url': os.environ.get('donation_img_url') or 'http://gevin-zone.igevin.info/pay-2.jpg?imageView/2/h/210'
    },
    'wechat': {
        'display_wechat': os.environ.get('display_wechat', 'true').lower() == 'true',
        'wechat_msg': get_env_value('wechat_msg', 'Welcome to follow my wechat'),
        'wechat_image_url': os.environ.get('wechat_image_url') or 'http://7tsygu.com1.z0.glb.clouddn.com/gevin-view.jpg?imageView/2/w/150',
        'wechat_title': get_env_value('wechat_title', 'GevinView'),
    },
    'copyright': {
        'display_copyright': os.environ.get('allow_display_copyright', 'true').lower() == 'true',
        'copyright_msg': get_env_value('copyright_msg', 'The article is not allowed to repost unless author authorized')
    },
    'only_abstract_in_feed': os.environ.get('only_abstract_in_feed', 'false').lower() == 'true',
    'allow_share_article': os.environ.get('allow_share_article', 'true').lower() == 'true',
    'allow_wechat_port': os.environ.get('allow_wechat_port', 'false').lower() == 'true',
    'gavatar_cdn_base': os.environ.get('gavatar_cdn_base', '//cdn.v2ex.com/gravatar/'),
    'gavatar_default_image': os.environ.get('gavatar_default_image', 'http://7tsygu.com1.z0.glb.clouddn.com/user-avatar.jpg'),
    'background_image': {
        'home': os.environ.get('bg_home') or 'http://7d9q7a.com1.z0.glb.clouddn.com/octblog-bg.jpg',
        'post': os.environ.get('bg_post') or 'http://7d9q7a.com1.z0.glb.clouddn.com/octblog-bg.jpg',
        'about': os.environ.get('bg_about') or 'http://7d9q7a.com1.z0.glb.clouddn.com/octblog_about.jpg',
        'qiniu': os.environ.get('qiniu') or 'http://assets.qiniu.com/qiniu-transparent.png',
    },
    'daovoice':{
        'allow_daovoice': (os.environ.get('allow_daovoice', 'false').lower() == 'true' and os.environ.get('daovoice_app_id') is not None),
        'app_id': os.environ.get('daovoice_app_id'),
    }

}

class Config(object):
    DEBUG = False
    TESTING = False

    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fjdljLJDL08_80jflKzcznv*c'
    MONGODB_SETTINGS = {'DB': 'OctBlog'}

    TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates').replace('\\', '/')
    STATIC_PATH = os.path.join(BASE_DIR, 'static').replace('\\', '/')
    EXPORT_PATH = os.path.join(BASE_DIR, 'exports').replace('\\', '/')

    if not os.path.exists(EXPORT_PATH):
        os.makedirs(EXPORT_PATH)

    REMEMBER_COOKIE_DURATION = datetime.timedelta(hours=3)


    #########################
    # email server
    #########################
    # MAIL_SERVER = 'smtp.gmail.com'
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.mxhichina.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 465))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'false').lower() == 'true'
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'true').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


    @staticmethod
    def init_app(app):
        pass

class DevConfig(Config):
    DEBUG = True

class PrdConfig(Config):
    # DEBUG = False
    DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'
    MONGODB_SETTINGS = {
            'db': os.environ.get('DB_NAME') or 'OctBlog',
            'host': os.environ.get('MONGO_HOST') or 'localhost',
            # 'port': 12345
        }

class TestingConfig(Config):
    TESTING = True
    DEBUG = True

    WTF_CSRF_ENABLED = False
    MONGODB_SETTINGS = {
        'db': 'OctBlogTest',
        'is_mock':True
        }

config = {
    'dev': DevConfig,
    'prd': PrdConfig,
    'testing': TestingConfig,
    'default': DevConfig,
}
