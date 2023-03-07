from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session, jsonify

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'oh-so-secret'

@app.route('/')
def index():
    """ Shows Homepage """

    return render_template('base.html')

@app.route('/board')
def show_board():
    """ Makes a new board, saves the new board to the session and then shows board """

    board = boggle_game.make_board()
    session['board'] = board

    return render_template('board.html', board=board)

@app.route('/check/<guess>', methods=["POST"])
def check_guess(guess):
    """ takes the form values and checks if the guess is a valid word, returns response as json """

    board = session['board']
    is_valid = boggle_game.check_valid_word(board, guess)
    res = jsonify(result=is_valid)

    return  res