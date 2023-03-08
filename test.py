from unittest import TestCase
from app import app
from flask import session, json
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def setUp(self):
        """ Do before every test """

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
        with self.client:
            res = self.client.get('/')
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Boggle</h1>', html)

    def test_show_board(self):
        with self.client:
            res = self.client.get('/board')
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<p>Result: </p>', html)

    def test_check_guess(self):
        with app.app_context():

            data = {'guess':'abc'}
            res = self.client.post('/check', json=data)

            self.assertEqual(res.status_code, 200)

    def test_update(self):
        with self.client:

            data = {'score': '10'}
            res = self.client.post('/update', json=data)

            self.assertEqual(res.status_code, 200)