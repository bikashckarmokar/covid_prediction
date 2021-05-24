from django.test import TestCase
import requests

HOME_API_URL = 'http://127.0.0.1:8000/'


class HomeApi(TestCase):
    '''
    Using postman these can be tested as well.
    '''

    def test_welcome(self):
        # python manage.py test home.tests.HomeApi.test_welcome

        response = requests.get(HOME_API_URL+'welcome/')
        content = response.content
        assert content == b'"Welcome to covid prediction service"'
