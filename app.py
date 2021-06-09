from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = 'gaspack'
debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
def home_page():
    return render_template('base.html')


@app.route('/questions/<int:num>')
def show_questions():
    return render_template('questions.html')
