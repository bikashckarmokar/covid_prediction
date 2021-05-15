import unittest

from django.test import TestCase
from django.test import tag

import requests


PREDICT_API_URL = 'http://127.0.0.1:8000/predict/'
SKIPT_TEST = True
REASON = 'Quick Test'


class PredictApi(TestCase):
    '''
    Using postman these can be tested as well.
    '''

    @tag('important')
    def test_predict_negative(self):
        # python manage.py test predict.tests.PredictApi.test_predict_negative

        data = {
            "cough": [0],
            "fever": [0],
            "sore_throat": [0],
            "shortness_of_breath": [0],
            "head_ache": [0],
            "age_60_and_above": [0],
            "gender": [0],
            "test_indication": [0]
        }

        response = requests.post(PREDICT_API_URL, json=data)
        results = response.json()

        assert results['corona'] == 0

    def test_predict_positive(self):
        # python manage.py test predict.tests.PredictApi.test_predict_positive

        data = {
            "cough": [1],
            "fever": [1],
            "sore_throat": [1],
            "shortness_of_breath": [1],
            "head_ache": [1],
            "age_60_and_above": [1],
            "gender": [1],
            "test_indication": [1]
        }

        response = requests.post(PREDICT_API_URL, json=data)
        results = response.json()

        assert results['corona'] == 1

    @unittest.skipIf(SKIPT_TEST, REASON)
    def test_predict_skip_test(self):
        # python manage.py test predict.tests.PredictApi.test_predict_positive

        data = {
            "cough": [0],
            "fever": [0],
            "sore_throat": [0],
            "shortness_of_breath": [0],
            "head_ache": [0],
            "age_60_and_above": [0],
            "gender": [0],
            "test_indication": [0]
        }

        response = requests.post(PREDICT_API_URL, json=data)
        results = response.json()

        assert results['corona'] == 0
