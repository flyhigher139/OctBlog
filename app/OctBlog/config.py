import os, sys

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
