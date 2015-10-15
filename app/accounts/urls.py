from flask import Blueprint

from . import views

accounts = Blueprint('accounts', __name__)

accounts.add_url_rule('/login/', 'login', views.login, methods=['GET', 'POST'])
accounts.add_url_rule('/logout/', 'logout', views.logout)
accounts.add_url_rule('/registration/', 'register', views.register, methods=['GET', 'POST'])
accounts.add_url_rule('/add-user/', 'add_user', views.add_user, methods=['GET', 'POST'])