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
        """ Ensures homepage response is status code 200 and response includes correct html"""

        with self.client:
            res = self.client.get('/')
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Boggle</h1>', html)

    def test_show_board(self):
        """ Ensures board page response is status code 200 and response includes correct html"""

        with self.client:
            res = self.client.get('/board')
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<p>Result: </p>', html)

    def test_check_guess(self):
        """ Ensures check guess route response is status code 200, board in session is set, and response result is ok when valid word in board is passed """

        with self.client:
            with self.client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"]]

            data = {'guess':'cat'}
            res = self.client.post('/check', json=data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(session['board'], [["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"]])
            self.assertEqual(res.json['result'], 'ok')

    def test_check_guess_not_on_board(self):
        """ Ensures check guess route response is status code 200, board in session is set, and response result is not-on-board when word not on board is passed"""

        with self.client:
            with self.client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"]]
                
            data = {'guess': 'dog'}
            res = self.client.post('/check', json=data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json['result'], 'not-on-board')

    def test_update(self):
        """ Ensures update route responds with status code 200 when score data is sent to server, and session is correctly updated with number of games played"""

        with self.client:
            with self.client.session_transaction() as change_session:
                change_session['games_played'] = 20

            data = {'score': '10'}
            res = self.client.post('/update', json=data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(session['games_played'], 21)
            self.assertEqual(res.json['gamesPlayed'], 21)
            self.assertEqual(int(res.json['score']), 10)
