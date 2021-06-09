from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.run(port=8080)


debug = DebugToolbarExtension(app)
responses = []


@app.route('/')
def show_home():
    return render_template('home.html', survey=survey)


@app.route('/start', methods=['POST'])
def start():
    return redirect('/questions/0')


@app.route('/questions/<int:qid>')
def show_questions(qid):
    if responses is None:
        return redirect('/')
    if len(responses) == len(survey.questions):
        return 'You have completed all of the survey questions'
    if len(responses) != len(qid):
        flash('invalid question id {qid}')
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question)


@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""

    return render_template("completion.html")
