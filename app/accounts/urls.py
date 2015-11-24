from flask import Blueprint

from . import views

accounts = Blueprint('accounts', __name__)

accounts.add_url_rule('/login/', 'login', views.login, methods=['GET', 'POST'])
accounts.add_url_rule('/logout/', 'logout', views.logout)
accounts.add_url_rule('/registration/', 'register', views.register, methods=['GET', 'POST'])
accounts.add_url_rule('/registration/su', 'register_su', views.register, defaults={'create_su':True}, methods=['GET', 'POST'])
accounts.add_url_rule('/add-user/', 'add_user', views.add_user, methods=['GET', 'POST'])
accounts.add_url_rule('/users/', view_func=views.Users.as_view('users'))
accounts.add_url_rule('/users/edit/<username>', view_func=views.User.as_view('edit_user'))