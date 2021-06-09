from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
reponses = []

debug = DebugToolbarExtension(app)


@app.route('/')
def show_home():
    return render_template('home.html', survey=survey)


@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

    # get the response choice
    choice = request.form['answer']

    # add this response to the session
    responses.append(choice)

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route('/start', methods=['POST'])
def start():
    return redirect('/questions/0')


@app.route('/questions/<int:qid>')
def show_questions(qid):
    if responses is None:
        return redirect('/')
    if len(responses) == len(survey.questions):
        return 'You have completed all of the survey questions'
    if len(responses) != qid:
        flash('invalid question id {qid}')
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template(
        "questions.html", question_num=qid, question=question)


@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""

    return render_template("completion.html")
