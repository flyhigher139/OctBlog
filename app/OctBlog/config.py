import os, sys

OctBlogSettings = {
    'allow_registration': True,
    'blog_meta': {
        'name': os.environ.get('name') or 'Oct Blog',
        'subtitle': os.environ.get('subtitle') or 'Oct Blog Subtitle',
        'description': os.environ.get('description') or 'Oct Blog Description',
        'owner': os.environ.get('owner') or 'Gevin',
        'keywords': os.environ.get('keywords') or 'python,django,flask,docker,MongoDB',
        'google_site_verification': '',
        'baidu_site_verification': '',
    },
    'pagination':{
        'per_page': int(os.environ.get('per_page', 5)),
        'admin_per_page': int(os.environ.get('admin_per_page', 10)),
    },
        
}

class Config(object):
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fjdljLJDL08_80jflKzcznv*c'
    MONGODB_SETTINGS = {'DB': 'OctBlog'}

    TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates').replace('\\', '/')
    STATIC_PATH = os.path.join(BASE_DIR, 'static').replace('\\', '/')


    @staticmethod
    def init_app(app):
        pass

class DevConfig(Config):
    DEBUG = True

class PrdConfig(Config):
    # DEBUG = False
    DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'
    MONGODB_SETTINGS = {
            'db': 'OctBlog',
            'host': os.environ.get('MONGO_HOST') or 'localhost',
            # 'port': 12345
        }


config = {
    'dev': DevConfig,
    'prd': PrdConfig,
    'default': DevConfig,
}
