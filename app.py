from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session, jsonify

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'oh-so-secret'

@app.route('/')
def index():
    """ Shows Homepage """

    games_played = session.get('games_played', 0)

    return render_template('base.html', games_played=games_played)

@app.route('/board')
def show_board():
    """ Makes a new board, saves the new board to the session and then shows board """

    board = boggle_game.make_board()
    session['board'] = board
    games_played = session.get('games_played', 0)

    return render_template('board.html', board=board, games_played=games_played)

@app.route('/check', methods=["POST"])
def check_guess():
    """ takes the form values and checks if the guess is a valid word, returns response as json """

    guess = (request.json)['guess']
    board = session['board']
    is_valid = boggle_game.check_valid_word(board, guess)
    res = jsonify(result=is_valid)

    return res

@app.route('/update', methods=["POST"])
def update_scores():
    """ receives the score at end of each game and increments the number of games played by 1 """

    session['games_played'] = session.get('games_played', 0) + 1
    score = (request.json)['score']

    return jsonify(gamesPlayed = session['games_played'])