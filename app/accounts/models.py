import datetime
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from OctBlog import db, login_manager

class User(UserMixin, db.Document):
    username = db.StringField(max_length=255, required=True)
    email = db.EmailField(max_length=255)
    password_hash = db.StringField(required=True)
    create_time = db.DateTimeField(default=datetime.datetime.now, required=True)
    last_login = db.DateTimeField(default=datetime.datetime.now, required=True)

    @property
    def password(self):
        raise AttributeError('password is not a readle attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        try:
            return unicode(self.username)
        except AttributeError:
            raise NotImplementedError('No `username` attribute - override `get_id`')


    
@login_manager.user_loader
def load_user(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    return user

