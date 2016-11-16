import unittest
from flask import current_app, url_for
from OctBlog import create_app, db
from accounts import models as accounts_models
from main import models as main_models


class ModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db_name = current_app.config['MONGODB_SETTINGS']['DB']
        db.connection.drop_database(db_name)
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue(response.status_code==200)

    # def test_register_and_login(self):
    #     response = self.client.post(url_for('accounts.register'), data={
    #         'username': 'octblog',
    #         'email': 'octblog@example.com',
    #         'password': 'octblog',
    #         'password2': 'octblog'
    #     })
    #
    #     self.app.logger.debug(response.status_code)
    #     self.assertTrue(response.status_code==302)
