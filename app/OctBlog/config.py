import os, sys

OctBlogSettings = {
    'allow_registration': True,
    'blog_meta': {
        'name': os.environ.get('name') or 'Oct Blog',
        'subtitle': os.environ.get('subtitle') or 'Oct Blog Subtitle',
        'description': os.environ.get('description') or 'Oct Blog Description',
        'owner': os.environ.get('owner') or 'Gevin',
        # 'keywords': [keyword.strip() for keyword in os.environ.get('keywords').split(',')] if os.environ.get('keywords') else ['python', 'Django', 'Flask', 'Docker', 'MongoDB'],
        'keywords': os.environ.get('keywords') or 'python,django,flask,docker,MongoDB',
        'google_site_verification': '',
        'baidu_site_verification': '',
    }
        
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

config = {
    'dev': DevConfig,
    'default': DevConfig
}
