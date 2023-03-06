from boggle import Boggle
from flask import Flask, request, render_template, redirect

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'oh-so-secret'

@app.route('/')
def index():
    return render_template('index.html')